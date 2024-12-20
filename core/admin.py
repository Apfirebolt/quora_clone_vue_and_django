from django.contrib import admin
from core.models import Question, Answer, Comment


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'content', 'created_at', 'updated_at']
    search_fields = ['author', 'slug', 'content']
    list_filter = ['author', 'slug', 'content', 'created_at', 'updated_at']
    list_per_page = 20


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['author', 'question', 'body', 'created_at', 'updated_at']
    search_fields = ['author', 'question', 'body']
    list_filter = ['author', 'question', 'body', 'created_at', 'updated_at']
    list_per_page = 20


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'answer', 'body', 'created_at', 'updated_at']
    search_fields = ['author', 'answer', 'body']
    list_filter = ['author', 'answer', 'body', 'created_at', 'updated_at']
    list_per_page = 20


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)



# Register your models here.
