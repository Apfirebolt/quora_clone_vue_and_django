import pika
import json
from django.conf import settings

def publish_login_event(user_data):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host=settings.RABBITMQ_VHOST,
        credentials=credentials,
    )
    
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # 1. Ensure the exchange exists (creates if not present)
        channel.exchange_declare(
            exchange=settings.RABBITMQ_EXCHANGE,
            exchange_type='topic',
            durable=True
        )

        # 2. Ensure the queue exists (creates if not present)
        login_queue_name = getattr(settings, 'RABBITMQ_LOGIN_QUEUE', 'login_notification_queue')
        channel.queue_declare(
            queue=login_queue_name,
            durable=True
        )

        # 3. Ensure the queue is bound to the exchange with the routing key
        channel.queue_bind(
            exchange=settings.RABBITMQ_EXCHANGE,
            queue=login_queue_name,
            routing_key="user.login"
        )

        # 4. Construct and publish the message
        message = json.dumps({
            "event": "user.login",
            "user_id": user_data.get("id"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
        })

        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key="user.login",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent on disk
                content_type='application/json'
            )
        )
        connection.close()
    except Exception as e:
        # Catch errors so RabbitMQ connectivity issues do not block the user login flow
        print(f"Failed to publish login event to RabbitMQ: {e}")