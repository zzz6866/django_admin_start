from __future__ import absolute_import

import os
from datetime import timedelta

from celery import Celery

# Django의 세팅 모듈을 Celery의 기본으로 사용하도록 등록합니다.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')

from django.conf import settings  # noqa

BROKER_URL = 'django://'
# CELERY_RESULT_BACKEND = 'db+postgresql://postgres:postgres@192.168.0.2/postgres'
CELERY_RESULT_BACKEND = 'django://'
app = Celery('myweb', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERY_IGNORE_RESULT=False
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
