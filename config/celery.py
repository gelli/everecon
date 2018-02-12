from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Including packages directly makes them fail in case of errors
# while autodiscover_tasks() fails silently... use me for debug
# app = Celery('everecon', include=['everecon.navigate.tasks'])
app = Celery('everecon')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
