# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from celery import shared_task
from celery.utils.log import get_task_logger

from namuh_bot.models import *

logger = get_task_logger(__name__)


@shared_task()
def get_stock_cd_list():  # 한국거래소에서 상장 종목 가져오기 (xls)
    logger.info("get_stock_cd_list START !!!!")
    stock_proc = StockProc.objects.get(id=1)
