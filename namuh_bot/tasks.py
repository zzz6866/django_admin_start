# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from djongo import models

from namuh_bot.models import StockCmdBaseCd

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 한국거래소에서 상장 종목 가져오기 (xls)
    logger.info("get_stock_cd_list START !!!!")
    # stock = StockCmdBaseCd.objects.get(cmd='connect').get_all_children()  # mptt 추천....
    # print(stock)
