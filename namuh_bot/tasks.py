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
    proc_login = model_to_dict(proc.login_info, exclude=['id', 'name'])

    param = [{'req_id': 'connect', 'param': proc_login}, {'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'p1005', 'szInput': '1', 'nInputLen': 1, 'nAccountIndex': 0}}]

    response = request_bot(param)

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
        proc_login = model_to_dict(proc.login_info, exclude=['id', 'name'])
        param = [{'req_id': 'connect', 'param': proc_login}]

        order = proc.procorder_set.first()
        if not order:
            return None
        else:
            if order.is_buy:  # 구매 후 단가 체크
                param.append({'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'c1101', 'szInput': 'K\x00' + order.buy_cd_id + '\x00', 'nInputLen': 8, 'nAccountIndex': 0}})  # 구매 및 시세 조회 쿼리
            else:  # 구매 처리 (미구매 상태)
                order.account_pw = proc_login['account_pw']
                struct = C8102InBlockStruct(order)
                param.append({'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'c8102', 'szInput': struct.get_bytes().decode('utf-8'), 'nInputLen': sizeof(struct), 'nAccountIndex': 1}})  # 매수

        response = request_bot(param)
        if response:
            # logger.debug(response.json())  # validation check
            # if any('c1101OutBlock2' in d for d in response.json()):
            #     cd_list = response.json()[0]['p1005OutBlock']
            for data in response.json():
                logger.debug(data)

    logger.info("get_today_flip_order END !!!!")


def request_bot(param):  # 봇에 데이터 요청
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://localhost:10003/namuh_windows'

    logger.debug(param)
    response = requests.post(url, headers=headers, json=param)

    logger.info(f"status_code : {response.status_code}")
    return response
