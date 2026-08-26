import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora_clone.settings')

app = Celery('quora_clone')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()