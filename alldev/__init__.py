from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# django_celery 사용시 tasks.py에 정의한 스케쥴에 대해 목록화를 위한 작업
from .celery import app as celery_app

__all__ = ('celery_app',)
