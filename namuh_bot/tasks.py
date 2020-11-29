# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
from ctypes import sizeof

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.forms import model_to_dict

from namuh_bot.models import Proc, CD
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
            if order.is_buy:  # 종가 단가 체크 후 조건 충족시 매도 처리
                if any('c1101OutBlock2' in d for d in response.json()):
                    out_block = find_json_elemnt(items=response.json(), name='c1101OutBlock2')
                    is_noon = time.strftime("%p")
                    logger.debug(f"{is_noon} : {out_block[0].get('time')} => {out_block[0].get('price')}")
                    valid = order.procvalid_set.get(is_noon=is_noon)
                    if valid:
                        for item in out_block:
                            if item.get('price') > valid.max_plus_value:
                                logger.debug('sell')
                                return  # 매도 처리
                            else:
                                logger.debug('not sell')
                    else:
                        logger.debug(f'no vaild : {is_noon}')

            else:  # 매수 요청 후 결과 처리
                if any('c8102OutBlock' in d for d in response.json()):  # 체결 완료 처리(이후 가격 체크)
                    out_block = find_json_elemnt(items=response.json(), name='c8102OutBlock')[0]
                    if out_block['order_noz10'] != '':
                        order.is_buy = True
                        order.save()
                    else:
                        result_msg = find_json_elemnt(items=response.json(), name='00000')
                        logger.debug('not buy!!! %s' % result_msg)

    logger.info("get_today_flip_order END !!!!")


def request_bot(param):  # 봇에 데이터 요청
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://localhost:10003/namuh_windows'

    # logger.debug(param)
    response = requests.post(url, headers=headers, json=param)

    logger.info(f"status_code : {response.status_code}")
    return response


# for (k, v) in data.items():
#    print("Key: " + k)
#    print("Value: " + str(v))
def find_json_elemnt(items, name):
    for data in items:
        if any(name == d for d in data):
            return data.get(name, None)
    return None
