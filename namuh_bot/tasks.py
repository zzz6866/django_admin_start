from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from namuh_bot.models import StockCd

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 한국거래소에서 상장 종목 가져오기 (xls)
    logger.info("get_stock_cd_list START !!!!")

    from bs4 import BeautifulSoup
    import urllib.request

    with urllib.request.urlopen('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download') as f:
        html = f.read().decode('euc-kr')

        soup = BeautifulSoup(html, 'html.parser')
        tr_list = soup.select("table.bbs_tb > tr")  #

        table_json = []
        colunms = [th.text for i, th in enumerate(tr_list[0].find_all("th"))]
        for tr in tr_list[1:]:
            row = {}
            for i, td in enumerate(tr.find_all("td")):
                row[colunms[i]] = td.text.strip()

            if row:
                table_json.append(row)

        for json in table_json:
            stock = StockCd()
            stock.cd = json["종목코드"]
            stock.nm = json["회사명"]
            stock.save()

        logger.info("get_stock_cd_list END !!!!")


@shared_task
def get_stock_price_list():  # 장 마감 이후 종가 조회
    stock_list = StockCd.objects.all()
    for i in stock_list:
        print(i)
