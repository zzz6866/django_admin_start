from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from torrent_bot.selenium_chrome import SeleniumChrome
from torrent_bot.telegram_bot import TelegramBot

logger = get_task_logger(__name__)


@shared_task
def find_new_torrent_movie():
    # Selenum을 통한 토렌트 수집
    selenium_chrome = SeleniumChrome()
    res_list = selenium_chrome.get_new_torrent_movie()

    # 텔레그램을 통한 수집된 토렌트에 대한 메시지 밣송
    bot = TelegramBot()
    bot.send_message_new_list(res_list)


@shared_task
def torrent_test_print(msg):
    logger.info(msg)
    # print(msg)
