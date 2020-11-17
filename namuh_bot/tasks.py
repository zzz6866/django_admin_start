# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from namuh_bot.models import StockProc, StockProcDtl, StockProcDtlVal, StockCd

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 한국거래소에서 상장 종목 가져오기 (xls)
    logger.info("get_stock_cd_list START !!!!")
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://localhost:10003/namuh_windows'
    param = []

    stock_proc = StockProc.objects.get(id=2)
    stock_proc_dtl = StockProcDtl.objects.filter(parent_id=stock_proc)
    for dtl in stock_proc_dtl:
        stock_proc_dtl_val = StockProcDtlVal.objects.filter(parent_id=dtl.id)
        # print(stock_proc_dtl_val.query)
        # {"req_id": "query", "param": {"nTRID": 1, "szTRCode": "p1005", "szInput": "1", "nInputLen": 1, "nAccountIndex": 0}}
        node = {'req_id': dtl.req_id, 'param': dict((dtl.values()) for dtl in stock_proc_dtl_val.values('key', 'val'))}
        # logger.debug(node)
        param.append(node)
        # dict((dtl.values()) for dtl in stock_proc_dtl.values('key', 'val'))

    response = requests.post(url, headers=headers, json=param)
    logger.info(f"status_code : {response.status_code}")
    # print(response.json())

    p1005OutBlock = response.json()[0]['p1005OutBlock']
    for node in p1005OutBlock:
        # print("node.code :", node.get('code'), " // node.hnamez40 :", node.get('hnamez40'))
        stock_cd = StockCd(cd=node.get('code'), nm=node.get('hnamez40'))
        stock_cd.save()

    logger.info(f"p1005OutBlock : SAVE {len(p1005OutBlock)}")
    logger.info("get_stock_cd_list END !!!!")

