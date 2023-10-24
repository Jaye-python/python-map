from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery

settings_file = 'local' if os.environ.get('IS_LOCAL') else 'production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdo_project.settings.' + settings_file)

app = Celery('pdo_project', broker=settings.CELERY_BROKER_URL)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.autodiscover_tasks()

#celery
app.conf.beat_schedule = {
    
    'send_live_signal':{
        'task': 'send_live_signal',
        'schedule': 5.0,
    },
        
} 