# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from namuh_bot.models import StockProc, StockProcDtl, StockProcDtlVal, StockCd

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 봇에서 상장 종목 가져오기 (dll call)
    logger.info("get_stock_cd_list START !!!!")

    stock_proc = StockProc.objects.filter(proc_type='A').first()
    response = request_bot(stock_proc)

    p1005OutBlock = response.json()[0]['p1005OutBlock']
    for node in p1005OutBlock:  # 종목 코드 저장
        logger.debug(f"code : {node.get('code')} => hnamez40 : {node.get('hnamez40')}")
        stock_cd = StockCd(cd=node.get('code'), nm=node.get('hnamez40'))
        stock_cd.save()

    logger.info(f"p1005OutBlock : SAVE {len(p1005OutBlock)}")
    logger.info("get_stock_cd_list END !!!!")


@shared_task()
def get_today_flip_order():  # 금일 단타 주문
    logger.info("get_today_flip_order START !!!!")

    stock_proc_list = StockProc.objects.filter(proc_type='B')  # 금일 단타 내역 조회
    for proc in stock_proc_list:
        response = request_bot(proc)
        if response:
            pass  # validation check

    logger.info("get_today_flip_order END !!!!")


def request_bot(stock_proc):  # 봇에 데이터 요청
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://localhost:10003/namuh_windows'
    param = []

    stock_proc_dtl = StockProcDtl.objects.filter(parent_id=stock_proc)
    response = None
    if stock_proc_dtl:
        for proc_dtl in stock_proc_dtl:
            stock_proc_dtl_val = StockProcDtlVal.objects.filter(parent_id=proc_dtl.id)
            # print(stock_proc_dtl_val.query)
            # {"req_id": "query", "param": {"nTRID": 1, "szTRCode": "p1005", "szInput": "1", "nInputLen": 1, "nAccountIndex": 0}}
            node = {'req_id': proc_dtl.req_id, 'param': dict((dtl.values()) for dtl in stock_proc_dtl_val.values('key', 'val'))}
            logger.debug(node)
            param.append(node)
            # dict((proc_dtl.values()) for proc_dtl in stock_proc_dtl.values('key', 'val'))
        response = requests.post(url, headers=headers, json=param)
        logger.info(f"status_code : {response.status_code}")
    return response
