from __future__ import absolute_import, unicode_literals
import os
from datetime import datetime

from celery import Celery

# set the default Django settings module for the 'celery' program.

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alldev.settings.production') # 환경 변수에 선언하여 사용하기 때문에 주석 처리
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')  # TODO: ValueError: not enough values to unpack (expected 3, got 0) <= 에러 발생으로 인한 추가
app = Celery('alldev')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: INSTALLED_APPS)

# Load task modules from all registered Django app configs.
# tasks.py 파일에 정의한 스케쥴에 대해 자동으로 목록화 한다. __init__.py 와 같이 사용 한다. 참고 - http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
app.autodiscover_tasks(packages=None)
# UTC FALSE 환경 설정시 시간차이가 발생하여 지정된 시간에 실행되지 않고 무한 반복 실행됨으로 인한 추가 설정
# app.now = datetime.now
# app.conf.timezone = 'Asia/Seoul'
# app.conf.enable_utc = False


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
# from __future__ import absolute_import
#
# import os
#
# from celery import Celery
#
# # Django의 세팅 모듈을 Celery의 기본으로 사용하도록 등록합니다.
# from coin_bot import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coin_bot.settings')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')  # TODO: ValueError: not enough values to unpack (expected 3, got 0) <= 에러 발생으로 인한 추가
#
# app = Celery('coin_bot', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
#
# # 문자열로 등록한 이유는 Celery Worker가 Windows를 사용할 경우
# # 객체를 pickle로 묶을 필요가 없다는 것을 알려주기 위함입니다.
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# # app.autodiscover_tasks()
#
#
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
#
#
# @app.task
# def testPrint(a, b, c):
#     print(a)
#     print(b)
#     print(c)
