from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from celery import shared_task, current_task
from celery.utils.log import get_task_logger

from torrent_bot.common import SeleniumChrome
from torrent_bot.models import TorrentMovie

logger = get_task_logger(__name__)


@shared_task
def find_new_torrent_movie():
    print('START SEARCH NEW MOVIE!!!')
    task_id = current_task.request.id
    base_url = 'https://torrentwal.com'
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

    # Chrome의 경우 아까 받은 chromedriver의 위치를 지정해준다.
    chromedriver = SeleniumChrome().driver
    # print(chromedriver_path) # chromedriver 프로그램 경로 또는 설치 경로

    # PhantomJS의 경우 아까 받은 PhantomJS의 위치를 지정해준다.
    # driver = webdriver.PhantomJS(executable_path=BASE_DIR + r'/selenium/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

    chromedriver.get(base_url + "/torrent_movie/torrent1.htm")
    html_list = chromedriver.page_source
    # print(html)
    soup = BeautifulSoup(html_list, 'html.parser')
    newest_table = soup.select('div#main_body > table.board_list > tbody > tr')  #
    # print(newest_table)
    for tr in newest_table:
        strong_today = tr.find('td', attrs={'class': 'datetime'}).find('strong', recursive=False)
        if strong_today or True:
            a_href = tr.find('td', attrs={'class': 'subject'}).find('a', recursive=False)
            detail_url = base_url + a_href['href'].replace('..', '')
            # 토렌트 idx 추출
            torrent_idx = a_href['href'].split('/')[-1].replace('.html', '')
            TorrentMovie.objects.get_or_create(torrent_id=torrent_idx,
                                               defaults={'torrent_movie_name': a_href.string, 'torrent_detail_url': detail_url, 'task_id': task_id})

            # print(torrent_idx)
            # chromedriver.get(detail_url)
            # html_detail = chromedriver.page_source
            # soup = BeautifulSoup(html_detail, 'html.parser')
            # table_file = soup.find('table', attrs={'id': 'file_table'}).find_all('tr')
            # print(table_file)
            # for i, detail_tr in enumerate(table_file):
            #     download_url = detail_tr.find('td').find('a', recursive=False)
            #     if download_url is not None and "magnet" not in str(download_url):
            #         print(i, "magnet" in str(download_url), download_url['href'])
            #         if "javascript" in str(download_url['href']).lower():
            #             print("javascript", )
            #         else:
            #             print("Not javascript")
            #
            #         chromedriver.find_element_by_css_selector('#file_table > tbody > tr:nth-child(' + str(i + 1) + ') > td > a').click()
    # Chrome Driver Close
    chromedriver.close()
