from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver

logger = get_task_logger(__name__)


@shared_task
def find_new_torrent():
    # print('START SEARCH NEW VIDEO!!!')
    # base_url = 'https://torrentwal.com'
    # res_list = requests.get(base_url + '/torrent_movie/torrent1.htm')
    # res_list.encoding = 'utf-8'
    # html = res_list.text
    # soup = BeautifulSoup(html, 'html.parser')
    # newest_table = soup.select('div#main_body > table.board_list > tr')
    # # print(newest_table[0])
    # for tr in newest_table:
    #     strong_today = tr.find('td', attrs={'class': 'datetime'}).find('strong', recursive=False)
    #     if strong_today:
    #         a_href = tr.find('td', attrs={'class': 'subject'}).find('a', recursive=False)['href']
    #         res_detail = requests.get(base_url + a_href.replace('..', ''))
    #         res_detail.encoding = 'utf-8'
    #         html = res_detail.text
    #         # print(html)
    #         soup = BeautifulSoup(html, 'html.parser')
    #         # table_file = soup.select('table#file_table')
    #         table_file = soup.find_all('table', attrs={'id': 'file_table'})
    #         print(table_file)

    # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    driver = webdriver.Chrome('/selenium/chromedriver_linux64/chromedriver')
    # PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
    driver = webdriver.PhantomJS('/selenium/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get("http://www.python.org")

    print(driver.current_url)
    print(driver.title)
    print(driver.page_source)


if __name__ == '__main__':
    find_new_torrent()
