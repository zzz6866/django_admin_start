import platform

from bs4 import BeautifulSoup
from celery import current_task
from celery.utils.log import get_task_logger
from selenium import webdriver

from alldev.settings.base import BASE_DIR
from torrent_bot.models import TorrentMovie

logger = get_task_logger(__name__)

BASE_URL = 'https://torrentwal.com'
TR_BOARD_LIST = 'div#blist > table.board_list > tbody > tr, div#main_body > table.board_list > tbody > tr'


class SeleniumChrome:
    """
    Selenim Chrome Init
    크롬으로 파싱을 위한 초기화
    """
    options = webdriver.ChromeOptions()  # chromedriver option 설정

    def __init__(self):
        self.options.add_argument('--headless')  # CLI 리눅스 사용을 위한 옵션 추가
        self.options.add_argument('--no-sandbox')  # CLI 리눅스 사용을 위한 옵션 추가
        self.options.add_argument('--disable-dev-shm-usage')  # CLI 리눅스 사용을 위한 옵션 추가
        # 크롬 창 사이즈
        # self.options.add_argument("--window-size=1000,500")

        if platform.system() == 'Windows':
            chromedriver_path = BASE_DIR + r"\selenium\chromedriver_win32\chromedriver"  # 프로그램 경로
            download_dir = BASE_DIR + r"\selenium\torrent_download"
        elif platform.system() == 'Darwin':
            # chromedriver_path = BASE_DIR + r"/selenium/chromedriver_mac64/chromedriver"
            chromedriver_path = r"/usr/local/bin/chromedriver"  # brew를 사용하여 패키지 설치한 경로
            download_dir = BASE_DIR + r"/selenium/torrent_download"
        else:
            chromedriver_path = r"/usr/bin/chromedriver"  # apt-get를 사용하여 패키지 설치한 경로
            download_dir = BASE_DIR + r"/selenium/torrent_download"
            self.options.binary_location = r"/usr/bin/google-chrome-stable"  # apt-get를 사용하여 패키지 설치한 경로

        # 파일 다운로드 설정
        self.options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        self.driver = webdriver.Chrome(chromedriver_path, chrome_options=self.options)

    def get_new_torrent_movie(self):
        """
        일일 신규 토렌트 조회 배치
        :return: task_id : celery task id
        """
        logger.info('START SEARCH NEW MOVIE!!!')
        task_id = current_task.request.id

        # Chrome의 경우 아까 받은 chromedriver의 위치를 지정해준다.
        chromedriver = self.driver
        # print(chromedriver_path) # chromedriver 프로그램 경로 또는 설치 경로

        # PhantomJS의 경우 아까 받은 PhantomJS의 위치를 지정해준다.
        # driver = webdriver.PhantomJS(executable_path=BASE_DIR + r'/selenium/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        page = 1
        res_list = []
        while True:
            get_url = BASE_URL + "/torrent_movie/torrent" + str(page) + ".htm"
            chromedriver.get(get_url)
            html_list = chromedriver.page_source
            # print(html)
            soup = BeautifulSoup(html_list, 'html.parser')
            tr_board_list = soup.select(TR_BOARD_LIST)  #
            # print(tr_board_list)
            for tr in tr_board_list:
                strong_today = tr.find('td', attrs={'class': 'datetime'}).find('strong', recursive=False)
                # strong_today = tr.find('td', attrs={'class': 'datetime'})
                if strong_today:
                    a_href = tr.find('td', attrs={'class': 'subject'}).find('a', recursive=False)
                    detail_url = BASE_URL + a_href['href'].replace('..', '')  # 상세 화면 url
                    dic = {"torrent_title": a_href.string, "torrent_detail_url": detail_url}
                    res_list.append(dic)

                    # 상세 화면에서 torrent or magnet url을 뽑아 다운로드 목록에 추가하는 로직 (미구현)
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
            if len(res_list) == 30 * page:
                page += 1
            else:
                break
        # Chrome Driver Close
        chromedriver.close()
        return res_list

    def get_find_torrent(self, find_text):
        """
        토렌트 검색 조회
        :return:
        """
        logger.info('START FIND NEW TORRENT!!!')

        chromedriver = self.driver
        chromedriver.get(BASE_URL + '/bbs/s-1-' + find_text)
        # print(chromedriver.current_url)
        html_list = chromedriver.page_source
        # print(html)
        soup = BeautifulSoup(html_list, 'html.parser')
        tr_board_list = soup.select(TR_BOARD_LIST)  #
        # print(tr_board_list)
        res_list = []
        for (i, entry) in enumerate(tr_board_list):
            a_href = entry.find('td', attrs={'class': 'subject'}).find_all('a', recursive=False)[1]  # 제목
            detail_url = BASE_URL + a_href['href'].replace('..', '')  # 상세 화면 url
            dic = {"torrent_title": a_href.string, "torrent_detail_url": detail_url}
            res_list.append(dic)

        chromedriver.close()
        return res_list
