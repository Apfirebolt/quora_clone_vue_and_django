import json
import logging
import pika
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------
# Helper: RabbitMQ Connection & Publisher
# -------------------------------------------------------------------------
def _get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
    )
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host=settings.RABBITMQ_VHOST,
        credentials=credentials,
        heartbeat=60,
        blocked_connection_timeout=300,
    )
    return pika.BlockingConnection(parameters)


def _publish_to_exchange(routing_key, payload, queue_name=None):
    """Utility to declare exchange/queue and publish persistent messages."""
    connection = None
    try:
        connection = _get_rabbitmq_connection()
        channel = connection.channel()

        # Ensure topic exchange exists
        channel.exchange_declare(
            exchange=settings.RABBITMQ_EXCHANGE,
            exchange_type="topic",
            durable=True,
        )

        # Optional: bind queue if specified
        if queue_name:
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(
                exchange=settings.RABBITMQ_EXCHANGE,
                queue=queue_name,
                routing_key=routing_key,
            )

        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent message
                content_type="application/json",
            ),
        )
    except Exception as exc:
        logger.error(f"RabbitMQ publishing error on key '{routing_key}': {exc}")
        raise exc
    finally:
        if connection and not connection.is_closed:
            connection.close()


# -------------------------------------------------------------------------
# Async Publisher Tasks (Called from DRF Views)
# -------------------------------------------------------------------------
@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def task_publish_login_event(self, user_data):
    """Publish login events to RabbitMQ."""
    try:
        queue_name = getattr(
            settings, "RABBITMQ_LOGIN_QUEUE", "login_notification_queue"
        )
        payload = {
            "event": "user.login",
            "user_id": user_data.get("id"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
        }
        _publish_to_exchange(
            routing_key="user.login", payload=payload, queue_name=queue_name
        )
    except Exception as exc:
        logger.error(f"Failed to publish login event: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def task_publish_profile_update_event(self, profile_data):
    """Publish profile update events to RabbitMQ."""
    try:
        queue_name = getattr(
            settings, "RABBITMQ_PROFILE_QUEUE", "profile_update_queue"
        )
        payload = {
            "event": "user.profile.updated",
            "data": profile_data,
        }
        _publish_to_exchange(
            routing_key="user.profile.updated",
            payload=payload,
            queue_name=queue_name,
        )
    except Exception as exc:
        logger.error(f"Failed to publish profile update event: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def task_publish_follow_event(self, event_type, follower_id, followed_user_id):
    """Publish follow/unfollow events to RabbitMQ."""
    try:
        User = get_user_model()
        follower = User.objects.get(id=follower_id)
        followed_user = User.objects.get(id=followed_user_id)

        queue_name = getattr(
            settings, "RABBITMQ_FOLLOW_QUEUE", "user_follow_queue"
        )
        payload = {
            "event": event_type,
            "follower": {
                "id": follower.id,
                "username": follower.username,
                "email": follower.email,
            },
            "followed_user": {
                "id": followed_user.id,
                "username": followed_user.username,
                "email": followed_user.email,
            },
        }
        _publish_to_exchange(
            routing_key=event_type, payload=payload, queue_name=queue_name
        )
    except Exception as exc:
        logger.error(f"Failed to publish follow event: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def task_publish_answer_notification(self, answer_id, question_id, author_id):
    """Publish answer event to notify the question owner."""
    try:
        from core.models import Question, Answer
        User = get_user_model()

        question = Question.objects.select_related("author").get(id=question_id)
        answer = Answer.objects.get(id=answer_id)
        author = User.objects.get(id=author_id)

        # Do not notify if the user is answering their own question
        if question.author.id == author.id:
            return

        queue_name = getattr(
            settings, "RABBITMQ_ANSWER_QUEUE", "answer_notification_queue"
        )
        routing_key = getattr(
            settings, "RABBITMQ_ANSWER_ROUTING_KEY", "question.replies"
        )

        payload = {
            "event": "question.answered",
            "recipient_id": question.author.id,
            "content": f"{author.username or author.email} answered your question: '{question.content[:50]}...'",
            "question_slug": question.slug,
            "answer_uuid": str(answer.uuid),
        }
        _publish_to_exchange(
            routing_key=routing_key, payload=payload, queue_name=queue_name
        )
    except Exception as exc:
        logger.error(f"Failed to publish answer notification: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def task_publish_comment_notification(self, comment_id, answer_id, author_id):
    """Publish comment event to notify the answer author."""
    try:
        from core.models import Answer, Comment
        User = get_user_model()

        answer = Answer.objects.select_related("author", "question").get(id=answer_id)
        comment = Comment.objects.get(id=comment_id)
        author = User.objects.get(id=author_id)

        if answer.author.id == author.id:
            return

        queue_name = getattr(
            settings, "RABBITMQ_COMMENT_QUEUE", "comment_queue"
        )
        routing_key = getattr(
            settings, "RABBITMQ_COMMENT_ROUTING_KEY", "answer.replies"
        )

        payload = {
            "event": "answer.commented",
            "recipient_id": answer.author.id,
            "content": f"{author.username or author.email} commented on your answer.",
            "question_slug": answer.question.slug,
            "comment_uuid": str(comment.uuid),
        }
        _publish_to_exchange(
            routing_key=routing_key, payload=payload, queue_name=queue_name
        )
    except Exception as exc:
        logger.error(f"Failed to publish comment notification: {exc}")
        raise self.retry(exc=exc)


# -------------------------------------------------------------------------
# Periodic Queue Consumer (Runs every 30s via Celery Beat)
# -------------------------------------------------------------------------
@shared_task
def consume_notification_queues_batch():
    """
    Periodically polls and drains up to 50 messages per queue,
    writing new notifications to the Django database matching the Notification model.
    """
    from core.models import Notification

    close_old_connections()
    connection = None

    # Queues to drain during this batch window
    queues_to_drain = [
        getattr(settings, "RABBITMQ_ANSWER_QUEUE", "answer_notification_queue"),
        getattr(settings, "RABBITMQ_COMMENT_QUEUE", "comment_queue"),
        getattr(settings, "RABBITMQ_FOLLOW_QUEUE", "user_follow_queue"),
    ]

    try:
        connection = _get_rabbitmq_connection()
        channel = connection.channel()
        User = get_user_model()

        for queue_name in queues_to_drain:
            # Declare to ensure queue exists before checking
            channel.queue_declare(queue=queue_name, durable=True)

            # Pull up to 50 messages per cycle
            for _ in range(50):
                method_frame, header_frame, body = channel.basic_get(
                    queue=queue_name, auto_ack=False
                )
                if method_frame is None:
                    break  # Queue is empty

                try:
                    payload = json.loads(body.decode("utf-8"))
                    event_type = payload.get("event")

                    if event_type == "question.answered":
                        recipient = User.objects.get(id=payload["recipient_id"])
                        Notification.objects.create(
                            recipient=recipient,
                            message=payload.get("content", ""),
                            category="question_reply",
                            is_read=False,
                        )

                    elif event_type == "answer.commented":
                        recipient = User.objects.get(id=payload["recipient_id"])
                        Notification.objects.create(
                            recipient=recipient,
                            message=payload.get("content", ""),
                            category="comment_reply",
                            is_read=False,
                        )

                    elif event_type == "user.followed":
                        followed_user = User.objects.get(
                            id=payload["followed_user"]["id"]
                        )
                        follower_name = (
                            payload["follower"]["username"]
                            or payload["follower"]["email"]
                        )
                        Notification.objects.create(
                            recipient=followed_user,
                            message=f"{follower_name} started following you.",
                            category="follow",
                            is_read=False,
                        )

                    # Acknowledge successfully stored message
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

                except User.DoesNotExist:
                    logger.warning(
                        f"Target user not found for message in {queue_name}. Discarding message."
                    )
                    # Discard message rather than requeuing indefinitely if the user was deleted
                    channel.basic_nack(
                        delivery_tag=method_frame.delivery_tag, requeue=False
                    )

                except Exception as proc_err:
                    logger.error(
                        f"Error processing message from {queue_name}: {proc_err}"
                    )
                    # Requeue for transient DB failures
                    channel.basic_nack(
                        delivery_tag=method_frame.delivery_tag, requeue=True
                    )

    except Exception as conn_err:
        logger.error(f"Failed during batch queue consumption: {conn_err}")
    finally:
        if connection and not connection.is_closed:
            connection.close()
        close_old_connections()