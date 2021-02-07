# -*- coding: utf-8 -*-
import platform

from celery.utils.log import get_task_logger
from selenium import webdriver

from alldev.settings.base import BASE_DIR

logger = get_task_logger(__name__)


class SeleniumBrowser:
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
            chromedriver_path = BASE_DIR + r"\selenium_browser\chromedriver_win32\chromedriver"  # 프로그램 경로
            download_dir = BASE_DIR + r"\selenium_browser\torrent_download"
        elif platform.system() == 'Darwin':
            # chromedriver_path = BASE_DIR + r"/selenium_browser/chromedriver_mac64/chromedriver"
            chromedriver_path = r"/usr/local/bin/chromedriver"  # brew를 사용하여 패키지 설치한 경로
            download_dir = BASE_DIR + r"/selenium_browser/torrent_download"
        else:
            chromedriver_path = r"/usr/bin/chromedriver"  # apt-get를 사용하여 패키지 설치한 경로
            download_dir = BASE_DIR + r"/selenium_browser/torrent_download"
            self.options.binary_location = r"/usr/bin/google-chrome-stable"  # apt-get를 사용하여 패키지 설치한 경로

        # 파일 다운로드 설정
        self.options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        self.driver = webdriver.Chrome(chromedriver_path, chrome_options=self.options)
