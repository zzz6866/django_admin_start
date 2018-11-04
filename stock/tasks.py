from __future__ import absolute_import
from celery import shared_task

from djcelery import celery


# @celery.task(name='tasks.add')
# def add(x, y):
#     return x + y


@celery.task
def sleeptask(i):
    from time import sleep
    sleep(i)
    return i


@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task
def xsum(numbers):
    return sum(numbers)


@shared_task
def getBitthumbTicker(apiKey="", apiSecret=""):
    print("======getBitthumbTicker START========")
