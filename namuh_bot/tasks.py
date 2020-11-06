# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from socket import gethostname

from celery import shared_task
from celery.utils.log import get_task_logger

from namuh_bot.client import Client
from namuh_bot.models import *

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 한국거래소에서 상장 종목 가져오기 (xls)
    logger.info("get_stock_cd_list START !!!!")

    client = Client(gethostname(), 10003, print_msg)

    stock_proc = StockProc.objects.get(id=1)
    stock_proc_dtl = StockProcDtl.objects.filter(parent_id=stock_proc)
    for dtl in stock_proc_dtl:
        stock_proc_dtl_val = StockProcDtlVal.objects.filter(parent_id=dtl.id)
        # print(stock_proc_dtl_val.query)
        # {"req_id": "query", "param": {"nTRID": 1, "szTRCode": "p1005", "szInput": "1", "nInputLen": 1, "nAccountIndex": 0}}
        send_json = {'req_id': dtl.req_id, "param": dict((dtl.values()) for dtl in stock_proc_dtl_val.values('key', 'val'))}
        result = client.send(send_json)
        print(result)


def print_msg(msg):
    print("message=", msg)
