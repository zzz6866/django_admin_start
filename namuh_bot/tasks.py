# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import re
import time
import urllib.parse
from ctypes import sizeof

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from celery.utils.log import get_task_logger
from django.forms import model_to_dict

from namuh_bot.models import Proc, CD, ProcOrder, ProcLogin, ProcValid
from namuh_bot.namuh_structure import C8102InBlockStruct, C8101InBlockStruct
from selenium_browser.selenium_browser import SeleniumBrowser

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 봇에서 상장 종목 가져오기 (dll call)
    logger.info("get_stock_cd_list START !!!!")

    proc_login = model_to_dict(ProcLogin.objects.get(id=1), exclude=['id', 'name'])  # 종목 수집용 계정 설정

    param = [
        create_namuh_bot_connect(param=proc_login),
        create_namuh_bot_query(tr_code='p1005', str_input='1', len_input=1)  # 상장 종목 조회
    ]

    response = request_bot(param)

    if response:
        if any('p1005OutBlock' in d for d in response.json()):
            cd_list = response.json().get('p1005OutBlock')
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

    proc_list = Proc.objects.filter(status=False)  # 금일 단타 내역 조회

    for proc in proc_list:
        proc_login = model_to_dict(proc.login_info, exclude=['id', 'name'])
        param = [create_namuh_bot_connect(param=proc_login)]

        order = proc.procorder_set.first()
        if not order:
            return None
        else:
            if order.is_buy:  # 체결 여부 : 구매 후 단가 체크
                param.append(create_namuh_bot_query(tr_code='c1101', str_input='K\x00' + order.buy_cd_id + '\x00', len_input=8))  # 구매 및 시세 조회 쿼리
            else:  # 구매 처리 (미구매 상태)
                order.account_pw = proc_login['account_pw']
                struct = C8102InBlockStruct(order)
                param.append(create_namuh_bot_query(tr_code='c8102', str_input=struct.get_bytes().decode('utf-8'), len_input=sizeof(struct)))  # 매수

        response = request_bot(param)
        if response:
            # logger.debug(response.json())  # validation check
            # if any('c1101OutBlock2' in d for d in response.json()):
            #     cd_list = response.json()[0]['p1005OutBlock']
            if order.is_buy:  # 종가 단가 체크 후 조건 충족시 매도 처리
                if any('c1101OutBlock2' in d for d in response.json()):
                    out_block = response.json().get('c1101OutBlock2')
                    is_noon = time.strftime("%p")
                    valid = order.procvalid_set.filter(is_noon=is_noon)
                    if valid:
                        logger.debug(f"max_plus_value = {valid[0].max_plus_value}")
                        for item in out_block:
                            logger.debug(f"{is_noon} : {item.get('time')} => {item.get('price')}")
                            if item.get('price') > valid[0].max_plus_value:
                                logger.debug('sell')
                                struct = C8101InBlockStruct(order.account_pw.encode('utf-8'), order.buy_cd_id.encode('utf-8'), str("%012d" % order.buy_qty).encode('utf-8'), str("%010d" % valid[0].max_plus_value).encode('utf-8'), b'00', b'', proc_login['account_pw'].encode('utf-8'), proc_login['trade_pw'].encode('utf-8'))
                                sell_param = [{'req_id': 'connect', 'param': proc_login}, {'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': 'c8102', 'szInput': struct.get_bytes().decode('utf-8'), 'nInputLen': sizeof(struct), 'nAccountIndex': 1}}]
                                sell_response = request_bot(sell_param)
                                proc.status = True  # 완료 처리
                                proc.save()
                                break  # 매도 처리
                            else:
                                logger.debug('not sell')
                    else:
                        logger.debug(f'no vaild : {is_noon}')
                else:  # 결과 메시지 처리
                    result_msg = response.json().get('00000')
                    logger.debug('not buy!!! %s' % result_msg)
            else:  # 매수 요청 후 결과 처리
                if any('c8102OutBlock' in d for d in response.json()):  # 체결 완료 처리(이후 가격 체크)
                    out_block = response.json().get('c8102OutBlock')[0]
                    if out_block['order_noz10'].strip() != '':
                        order.is_buy = True
                        order.order_no = out_block['order_noz10']
                        order.save()
                    else:
                        result_msg = response.json().get('00000')
                        logger.debug('not buy!!! %s' % result_msg)
                else:
                    result_msg = response.json().get('00001')
                    logger.debug('result !!! %s' % result_msg)

    logger.info("get_today_flip_order END !!!!")


def request_bot(param):  # 봇에 데이터 요청
    hostname = os.environ.get('namuh_bot_ip')

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = 'http://' + hostname + ':10003/namuh_windows'

    # logger.debug(param)
    response = requests.post(url, headers=headers, json=param)

    logger.info(f"status_code : {response.status_code}")
    return response


# for (k, v) in data.items():
#    print("Key: " + k)
#    print("Value: " + str(v))
# def find_json_elemnt(items, name):  # response 결과에서 해당 데이터 찾기
#     for data in items:
#         if any(name == d for d in data):
#             return data.get(name, None)
#     return None


def create_namuh_bot_query(tr_code=None, str_input=None, len_input=0, account_index=0):  # query 정보 생성(시세조회, 주문정보 조회 등)
    return {'req_id': 'query', 'param': {'nTRID': 1, 'szTRCode': tr_code, 'szInput': str_input, 'nInputLen': len_input, 'nAccountIndex': account_index}}


def create_namuh_bot_connect(param=None):  # 로그인 정보 생성
    return {'req_id': 'connect', 'param': param}


@shared_task()
def get_today_trade_high_list():  # ## 네이버 거래량 급증 데이터 수집 처리
    logger.info("get_today_flip_order START !!!!")

    chromedriver = SeleniumBrowser().driver

    # 코스피
    chromedriver.get('https://finance.naver.com/sise/field_submit.nhn?menu=quant_high&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_quant_high.nhn%3Fsosok%3D0&fieldIds=quant&fieldIds=ask_buy&fieldIds=operating_profit&fieldIds=per&fieldIds=ask_sell&fieldIds=prev_quant')
    json_table = []
    # print(chromedriver.current_url)
    get_html_to_list(chromedriver, json_table, 'P')

    # 코스닥
    chromedriver.get('https://finance.naver.com/sise/field_submit.nhn?menu=quant_high&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_quant_high.nhn%3Fsosok%3D1&fieldIds=quant&fieldIds=ask_buy&fieldIds=operating_profit&fieldIds=per&fieldIds=ask_sell&fieldIds=prev_quant')
    get_html_to_list(chromedriver, json_table, 'D')

    # header : ['N', '증가율', '종목명', '현재가', '전일비', '등락률', '거래량', '전일거래량', '매수호가', '매도호가', '영업이익', 'PER']
    json_table.sort(key=lambda r: (-r[1], -r[6]))  # 기준 정렬
    # [logger.debug(row) for row in json_table]

    for row in json_table[:10]:
        buy_cd = row[0].split('-')[2]  # 종목코드
        chk_proc_order = Proc.objects.filter(procorder__buy_cd=buy_cd, status=False)
        if chk_proc_order.count() == 0 and False:  # 거래 목록에 이미 있을 경우 저장하지 않음
            new_proc = Proc.objects.create(name='네이버 거래량 급증 - ' + row[2], login_info_id=1)
            new_proc.save()

            new_proc_order = ProcOrder.objects.create(parent_id=new_proc.id, buy_cd_id=buy_cd, buy_price=row[3], buy_qty=1)
            new_proc_order.save()

            new_proc_valid = ProcValid.objects.create(is_noon='AM', plus_value=1.5, plus_type_code='P', parent_id=new_proc_order.id)
            new_proc_valid.save()

            new_proc_valid.id = None
            new_proc_valid.is_noon = 'PM'
            new_proc_valid.save()

    chromedriver.close()
    logger.info("get_today_flip_order END !!!!")


def get_html_to_list(chromedriver=None, json_table=None, sosok=''):  # 네이버 거래량 급증 화면 pare
    str_html = chromedriver.page_source
    # logger.debug(str_html)
    soup = BeautifulSoup(str_html, 'html.parser')
    result_table = soup.select('table.type_2 > tbody > tr')  #
    for row in result_table[1:]:
        if row.text != '':
            td_data = []
            for i, cell in enumerate(row('td')):
                try:
                    if i == 2:
                        href = cell.find('a')['href']
                        query_str = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                        td_data[0] += '-' + query_str['code'][0]

                    if i == 0:
                        value = sosok + '-' + cell.text
                    elif not bool(re.match('[a-zA-Z가-힣_]', cell.text)):
                        sub_value = re.sub(r'[^\d.]', '', cell.text)
                        value = float(sub_value)
                        if '.' not in sub_value:
                            value = int(sub_value)
                    else:
                        value = cell.text.strip()
                except ValueError as e:
                    value = cell.text.strip()
                td_data.append(value)
            json_table.append(td_data)
