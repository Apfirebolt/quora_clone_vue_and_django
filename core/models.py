import uuid as uuid_lib

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
    

