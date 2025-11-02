import pika
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import Notification


User = get_user_model()
EXCHANGE_NAME = settings.RABBITMQ_EXCHANGE
ROUTING_KEY = "answer.created"


def answer_callback(ch, method, properties, body):
    """
    Processes messages received on the answer.created queue.
    Creates a Notification if the answer is for another user's question.
    """
    try:
        # 1. Parse the incoming message
        message_data = json.loads(body)

        answer_author_id = message_data.get("answer_author_id")
        question_author_id = message_data.get("question_author_id")
        question_content = message_data.get("question_content")
        answer_content = message_data.get("answer_content")

        # 2. Check if the question author and answer author are different
        if answer_author_id != question_author_id:
            try:
                # Fetch the recipient (Question Author) and Answer Author
                recipient = User.objects.get(id=question_author_id)
                answer_author = User.objects.get(id=answer_author_id)

                # Construct the notification message
                message = (
                    f"**{answer_author.username}** answered your question: "
                    f"**'{question_content[:50].strip()}...'**"
                )

                # 3. Create the Notification record
                Notification.objects.create(
                    recipient=recipient, message=message, category="NEW_ANSWER"
                )
                print(f" [x] Notification created for {recipient.username}")

            except User.DoesNotExist:
                print(
                    f" [!] User not found (ID: {question_author_id} or {answer_author_id}). Skipping notification."
                )
            except Exception as db_e:
                print(
                    f" [!] Database Error creating notification: {db_e}. Requeuing message."
                )
                # Reject and requeue message if DB operation fails (e.g., transient error)
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
                return  # Exit callback to prevent acking

        else:
            print(" [x] Answered own question. No notification created.")

        # 4. Acknowledge the message ONLY after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        print(f" [!] Failed to decode JSON message: {body}. Discarding message.")
        ch.basic_reject(
            delivery_tag=method.delivery_tag, requeue=False
        )  # Don't requeue corrupted messages
    except Exception as e:
        print(f" [!] Unhandled error in callback: {e}. Discarding message.")
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


class Command(BaseCommand):
    help = "Runs the RabbitMQ consumer to process answers and generate notifications."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting RabbitMQ Consumer..."))

        try:
            # Establish connection
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

            channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")

            result = channel.queue_declare(
                queue=settings.RABBITMQ_QUEUE, durable=True
            )
            queue_name = result.method.queue

            channel.queue_bind(
                exchange=EXCHANGE_NAME, queue=queue_name, routing_key=ROUTING_KEY
            )

            self.stdout.write(
                f" [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C"
            )

            # 3. Start consuming messages using the defined callback
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=answer_callback,
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
