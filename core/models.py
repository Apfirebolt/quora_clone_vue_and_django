import uuid as uuid_lib
import pika
import json
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    content = models.CharField(max_length=240)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions"
    )
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="upvoted_questions", blank=True
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="downvoted_questions", blank=True
    )
    tags = models.ManyToManyField("Tag", related_name="questions", blank=True)

    def __str__(self):
        return self.content
    

class Answer(TimeStampedModel):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    body = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="upvoted_answers", blank=True
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="downvoted_answers", blank=True
    )

    def __str__(self):
        return self.author.username
    

class Comment(TimeStampedModel):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    body = models.TextField()
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Notification(TimeStampedModel):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message} ({self.category})"


@receiver(post_save, sender=Comment)
def comment_replied_handler(sender, instance, created, **kwargs):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD),
            virtual_host=settings.RABBITMQ_VHOST
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)

    message_data = {
        'comment_id': instance.id,
        'user_id': instance.author.id,
        'answer_user_id': instance.answer.author.id,
        'content': instance.body[:100], 
        'timestamp': str(instance.created_at)
        # Add any other relevant information
    }
    message = json.dumps(message_data)

    channel.basic_publish(
        exchange=settings.RABBITMQ_EXCHANGE,
        routing_key=settings.RABBITMQ_COMMENT_ROUTING_KEY,
        body=message
    )
    print(f"[x] Sent '{message}'")
    print('Exchange and routing key used:', settings.RABBITMQ_EXCHANGE, 'reply')
    connection.close()


@receiver(post_save, sender=Answer)
def answer_notification_handler(sender, instance, created, **kwargs):
    if created:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD),
                virtual_host=settings.RABBITMQ_VHOST
            )
        )
        channel = connection.channel()

        channel.exchange_declare(exchange=settings.RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)

        message_data = {
            'answer_id': instance.id,
            'question_id': instance.question.id,
            'question_author_id': instance.question.author.id,
            'answer_author_id': instance.author.id,
            'answer_content': instance.body[:100],
            'question_content': instance.question.content,
            'timestamp': str(instance.created_at)
        }
        message = json.dumps(message_data)

        channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key=settings.RABBITMQ_ANSWER_ROUTING_KEY,
            body=message
        )

        print(f"[x] Sent answer notification: '{message}'")
        connection.close()


