# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.forms import model_to_dict

from namuh_bot.models import StockProc, StockProcDtl, StockProcDtlVal, StockCd

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 봇에서 상장 종목 가져오기 (dll call)
    logger.info("get_stock_cd_list START !!!!")

    stock_proc = StockProc.objects.filter(proc_type='A').first()
    response = request_bot(stock_proc)

    if response:
        stock_list = response.json()[0]['p1005OutBlock']
        for node in stock_list:  # 종목 코드 저장
            logger.debug(f"code : {node.get('code')} => hnamez40 : {node.get('hnamez40')}")
            stock_cd = StockCd(cd=node.get('code'), nm=node.get('hnamez40'))
            stock_cd.save()
        logger.info(f"p1005OutBlock : SAVE {len(stock_list)}")

    logger.info("get_stock_cd_list END !!!!")


@shared_task()
def get_today_flip_order():  # 금일 단타 주문
    logger.info("get_today_flip_order START !!!!")

    stock_proc_list = StockProc.objects.filter(proc_type='B')  # 금일 단타 내역 조회
    for proc in stock_proc_list:
        response = request_bot(proc)
        if response:
            logger.debug(response.json())  # validation check

    logger.info("get_today_flip_order END !!!!")


def request_bot(stock_proc):  # 봇에 데이터 요청
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://localhost:10003/namuh_windows'
    param = []

    proc_dtl_list = stock_proc.stockprocdtl_set.all()
    # logger.debug(f"proc_dtl_list : {proc_dtl_list.values('req_id')}")
    # res.append(list(proc_dtl_list.values('req_id')))
    # proc_dict = model_to_dict(stock_proc, exclude=['id', 'proc_type', 'status'])
    for proc_dtl in proc_dtl_list:
        proc_dtl_val_list = proc_dtl.stockprocdtlval_set.all()
        proc_dtl_dict = model_to_dict(proc_dtl, exclude=['id', 'parent'])
        proc_dtl_val_dict = dict((val.values()) for val in proc_dtl_val_list.values('key', 'val'))
        if not proc_dtl_val_dict:  # key val 구조의 값이 없을 경우 봇을 call 하지 않음
            return None
        proc_dtl_dict.update({"param": proc_dtl_val_dict})
        # logger.debug(f"proc_dtl : {proc_dtl_dict}")
        param.append(proc_dtl_dict)
    logger.debug(param)
    response = requests.post(url, headers=headers, json=param)

    logger.info(f"status_code : {response.status_code}")
    return response
