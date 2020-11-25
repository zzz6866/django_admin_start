# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ctypes import sizeof

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.forms import model_to_dict
from mirage.crypto import Crypto

from alldev.settings.base import SECRET_KEY
from namuh_bot.models import Proc, CD, ProcOrder
from namuh_bot.namuh_structure import C8102InBlockStruct

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 봇에서 상장 종목 가져오기 (dll call)
    logger.info("get_stock_cd_list START !!!!")

    proc = Proc.objects.filter(type_code='A').first()
    response = request_bot(proc)

    if response:
        if any('p1005OutBlock' in d for d in response.json()):
            cd_list = response.json()[0]['p1005OutBlock']
            for node in cd_list:  # 종목 코드 저장
                logger.debug(f"code : {node.get('code')} => hnamez40 : {node.get('hnamez40')}")
                stock_cd = CD(cd=node.get('code'), nm=node.get('hnamez40'))
                stock_cd.save()
            logger.info(f"p1005OutBlock : SAVE {len(cd_list)}")
        else:
            logger.info('no data')

    logger.info("get_stock_cd_list END !!!!")


@shared_task()
def get_today_flip_order():  # 금일 단타 주문
    logger.info("get_today_flip_order START !!!!")

    proc_list = Proc.objects.filter(type_code='B', status=False)  # 금일 단타 내역 조회
    for proc in proc_list:
        response = request_bot(proc)
        if response:
            logger.debug(response.json())  # validation check

    logger.info("get_today_flip_order END !!!!")


def request_bot(proc):  # 봇에 데이터 요청
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://localhost:10003/namuh_windows'
    param = []

    # proc_dtl_list = proc.stockprocdtl_set.all()
    # logger.debug(f"proc_dtl_list : {proc_dtl_list.values('req_id')}")
    # res.append(list(proc_dtl_list.values('req_id')))
    # proc_dict = model_to_dict(stock_proc, exclude=['id', 'type_code', 'status'])
    # for proc_dtl in proc_dtl_list:
    #     proc_dtl_val_list = proc_dtl.stockprocdtlval_set.all()
    #     proc_dtl_dict = model_to_dict(proc_dtl, exclude=['id', 'parent'])
    #     proc_dtl_val_dict = dict((val.values()) for val in proc_dtl_val_list.values('key', 'val'))
    #     if not proc_dtl_val_dict:  # key val 구조의 값이 없을 경우 봇을 call 하지 않음
    #         return None
    #     proc_dtl_dict.update({"param": proc_dtl_val_dict})
    #    # logger.debug(f"proc_dtl : {proc_dtl_dict}")
    #     param.append(proc_dtl_dict)

    # {"req_id": "query", "param": {"nTRID": 1, "szTRCode": "p1005", "szInput": "1", "nInputLen": 1, "nAccountIndex": 0}}
    proc_login = model_to_dict(proc.login_info, exclude=['id', 'name'])
    param.append({'req_id': 'connect', 'param': proc_login})  # 로그인 정보

    if proc.type_code == 'A':  # 상장 종목 조회
        param.append({'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'p1005', 'szInput': '1', 'nInputLen': 1, 'nAccountIndex': 0}})  # 종목 코드 조회 쿼리
    elif proc.type_code == 'B':  # 체결 및 모니터링
        orders = proc.procorder_set.all()
        for order in orders:
            if order.is_buy:  # 구매 후 단가 체크
                param.append({'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'c1101', 'szInput': 'K ' + order.buy_cd_id + ' ', 'nInputLen': 8, 'nAccountIndex': 0}})  # 구매 및 시세 조회 쿼리
            else:  # 구매 처리 (미구매 상태)
                order.account_pw = proc_login['account_pw']
                struct = C8102InBlockStruct(order)
                param.append({'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'c8102', 'szInput': struct.get_bytes(), 'nInputLen': sizeof(struct), 'nAccountIndex': 1}})  # 매수
    else:
        return None
    logger.debug(param)
    response = requests.post(url, headers=headers, json=param)

    logger.info(f"status_code : {response.status_code}")
    return response
