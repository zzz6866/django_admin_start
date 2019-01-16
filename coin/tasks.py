from __future__ import absolute_import, unicode_literals
from celery import task
from celery.utils.log import get_task_logger

from .XCoinApiClient import XCoinAPI
from .models import PublicTicker as publicTicker


logger = get_task_logger(__name__)

@task
def getPublicTicker(apiKey, apiSecret):
    print("getPublicTicker START!")
    api = XCoinAPI(apiKey, apiSecret)

    # rgParams = { # parameter 불필요
    #     "order_currency": "ALL",
    #     "payment_currency": "KRW"
    # }

    #
    # public api
    # /public/ticker/{currency} 거래소 마지막 거래 정보
    # /public/orderbook/{currency} 거래소 판/구매 등록 대기 또는 거래 중 내역 정보
    # /public/recent_transactions/{currency} 거래소 거래 체결 완료 내역 (변경 전, 5월 23일까지 서비스)
    # /public/transaction_history/{currency} 거래소 거래 체결 완료 내역 (변경 후)
    # /public/btci bithumb 지수 (BTMI,BTAI)

    results = api.xcoinApiCall("/public/ticker/ALL", {})
    # print(results['status'])

    for (k, v) in results['data'].items():
        # print(v)
        if k != 'date' and len(v) > 0:
            date = results['data']['date']
            # print(date)
            # print("k: " + k)
            publicTicker.jsonToModel(coinCode=k, json=v, date=date)

        # else:
        #     print('--------------' + k + '---------------')
        #     print("last: " + v["closing_price"])
        #     print("sell: " + v["sell_price"])
        #     print("buy: " + v["buy_price"])
