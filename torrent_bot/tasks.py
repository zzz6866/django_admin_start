# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# from bs4 import BeautifulSoup
# from celery import shared_task
from celery.utils.log import get_task_logger

# from selenium_browser.selenium_browser import SeleniumBrowser
# from torrent_bot.telegram_bot import TelegramBot

logger = get_task_logger(__name__)

BASE_URL = 'https://torrentwal.com'
TR_BOARD_LIST = 'div#blist > table.board_list > tbody > tr, div#main_body > table.board_list > tbody > tr'


# @shared_task
# def find_new_torrent_movie():  # TODO : 사이트 사망으로 주석 처리
#     """
#     일일 신규 토렌트 조회 배치
#     :return: task_id : celery task id
#     """
#     logger.info('START SEARCH NEW MOVIE!!!')
#
#     # Selenum을 통한 토렌트 수집
#     # Chrome의 경우 아까 받은 chromedriver의 위치를 지정해준다.
#     chromedriver = SeleniumBrowser().driver
#     # print(chromedriver_path) # chromedriver 프로그램 경로 또는 설치 경로
#
#     # PhantomJS의 경우 아까 받은 PhantomJS의 위치를 지정해준다.
#     # driver = webdriver.PhantomJS(executable_path=BASE_DIR + r'/selenium_browser/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#     page = 1
#     res_list = []
#     while True:
#         get_url = BASE_URL + "/torrent_movie/torrent" + str(page) + ".htm"
#         chromedriver.get(get_url)
#         html_list = chromedriver.page_source
#         # print(html)
#         soup = BeautifulSoup(html_list, 'html.parser')
#         tr_board_list = soup.select(TR_BOARD_LIST)  #
#         # print(tr_board_list)
#         for tr in tr_board_list:
#             strong_today = tr.find('td', attrs={'class': 'datetime'}).find('strong', recursive=False)
#             # strong_today = tr.find('td', attrs={'class': 'datetime'})
#             if strong_today:
#                 a_href = tr.find('td', attrs={'class': 'subject'}).find('a', recursive=False)
#                 detail_url = BASE_URL + a_href['href'].replace('..', '')  # 상세 화면 url
#                 dic = {"torrent_title": a_href.string, "torrent_detail_url": detail_url}
#                 res_list.append(dic)
#
#                 # 상세 화면에서 torrent or magnet url을 뽑아 다운로드 목록에 추가하는 로직 (미구현)
#                 # print(torrent_idx)
#                 # chromedriver.get(detail_url)
#                 # html_detail = chromedriver.page_source
#                 # soup = BeautifulSoup(html_detail, 'html.parser')
#                 # table_file = soup.find('table', attrs={'id': 'file_table'}).find_all('tr')
#                 # print(table_file)
#                 # for i, detail_tr in enumerate(table_file):
#                 #     download_url = detail_tr.find('td').find('a', recursive=False)
#                 #     if download_url is not None and "magnet" not in str(download_url):
#                 #         print(i, "magnet" in str(download_url), download_url['href'])
#                 #         if "javascript" in str(download_url['href']).lower():
#                 #             print("javascript", )
#                 #         else:
#                 #             print("Not javascript")
#                 #
#                 #         chromedriver.find_element_by_css_selector('#file_table > tbody > tr:nth-child(' + str(i + 1) + ') > td > a').click()
#         if len(res_list) == 30 * page:
#             page += 1
#         else:
#             break
#     # Chrome Driver Close
#     chromedriver.close()
#
#     # 텔레그램을 통한 수집된 토렌트에 대한 메시지 밣송
#     bot = TelegramBot()
#     bot.send_message_new_list(res_list)
#
#     logger.info('END SEARCH NEW MOVIE!!!')
