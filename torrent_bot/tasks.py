from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
# from selenium import webdriver

logger = get_task_logger(__name__)


@shared_task
def search_new_video():
    print("START SEARCH NEW VIDEO!!!")

    # browser = webdriver.Chrome()
    # chromedriver가 Python파일과 같은 위치에 있거나, 혹은 OS의 PATH에 등록되어 쉘에서 실행 가능한 경우 위와같이 한다.
    # 혹은 browser = webdriver.Chrome('/path/to/chromedriver')의 절대경로로 해도 된다.
    # browser.get('http://localhost:8000')
