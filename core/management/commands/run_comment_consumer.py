import pika
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import Notification


User = get_user_model()
EXCHANGE_NAME = settings.RABBITMQ_EXCHANGE
COMMENT_QUEUE = settings.RABBITMQ_COMMENT_QUEUE

def comment_callback(ch, method, properties, body):
    """
    Processes messages received on the answer.created queue.
    Creates a Notification if the answer is for another user's question.
    """
    try:
        # 1. Parse the incoming message
        message_data = json.loads(body)

        user_id = message_data.get("user_id")
        answer_user_id = message_data.get("answer_user_id")
        content = message_data.get("content")
        
        # Check if the message is already processed (though usually managed by broker, good for idempotency)
        if user_id == answer_user_id:
            print(" [x] Commented on own answer. No notification created.")
            # Acknowledge and discard message as no further action is needed
            ch.basic_ack(delivery_tag=method.delivery_tag) 
            return

        # Use transaction.atomic to ensure the DB operation is successful before ack
        with transaction.atomic():
            
            # 2. Check if the comment author and answer author are different
            recipient = User.objects.get(id=answer_user_id)
            comment_author = User.objects.get(id=user_id)

            # Construct the notification message
            message = (
                f"**{comment_author.username or comment_author.email}** commented on your answer: "
                f"**'{content[:50].strip()}...'**"
            )

            # 3. Create the Notification record
            Notification.objects.create(
                recipient=recipient, message=message, category="NEW_COMMENT"
            )
            print(f" [x] Notification created for {recipient.username}")
        
        # 4. Acknowledge the message ONLY after the transaction/DB operation is successful
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except json.JSONDecodeError:
        print(f" [!] Failed to decode JSON message: {body}. Discarding message.")
        # Reject and don't requeue corrupted messages
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False) 
    
    except User.DoesNotExist:
        # If user is not found, discard the message (it won't magically appear later)
        print(
            f" [!] User not found (ID: {user_id} or {answer_user_id}). Discarding message."
        )
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        
    except Exception as e:
        # Any other error (e.g., transient DB error, network issue) -> REQUEUE
        print(
            f" [!] Unhandled error in callback: {e}. Requeuing message."
        )
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)


class Command(BaseCommand):
    help = "Runs the RabbitMQ consumer to process answers and generate notifications."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting RabbitMQ Consumer..."))

        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(
                        settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
                    ),
                    virtual_host=settings.RABBITMQ_VHOST,
                )
            )
            channel = connection.channel()

            channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

            result = channel.queue_declare(
                queue=COMMENT_QUEUE, durable=True
            )
            queue_name = result.method.queue

            channel.queue_bind(
                exchange=EXCHANGE_NAME, queue=queue_name, routing_key=settings.RABBITMQ_COMMENT_ROUTING_KEY
            )

            self.stdout.write(
                f" [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C"
            )

            # 3. Start consuming
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=comment_callback,
                auto_ack=False,  # Use manual acknowledgment for reliability
            )

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            self.stderr.write(
                self.style.ERROR(
                    "Could not connect to RabbitMQ. Check connection parameters and service status."
                )
            )
        except KeyboardInterrupt:
            self.stdout.write("\n [x] Consumer gracefully stopped.")
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Consumer failed with an unhandled error: {e}")
            )
        finally:
            # Ensure connection is closed if it was opened
            if "connection" in locals() and connection.is_open:
                connection.close()
