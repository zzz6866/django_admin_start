import json
from datetime import datetime

import telegram
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
from telegram import ParseMode

from torrent_bot.models import TorrentMovie, TelegramBotEnableStatus

logger = get_task_logger(__name__)

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '763953984:AAHZYhC_K5g8c11skZglFdohl6j9JX2t6Hs'

# 봇이 응답할 명령어
BUTTON_START = '/start'
BUTTON_STOP = '/stop'
BUTTON_HELP = '/help'
BUTTON_NEW_LIST_TORRNET = '/button_new_list_torrnet'
BUTTON_FIND_TORRNET = '/button_find_torrnet'

# 봇 사용법 & 메시지
USAGE = u"""[사용법] 아래 명령어를 메시지로 보내거나 버튼을 누르시면 됩니다.
        /start - (봇 활성화)
        /stop  - (봇 비활성화)
        /help  - (도움말)
        /button_new_list_torrnet  - (신규 토렌트 영화 목록)
        /button_find_torrnet  - (토렌트 검색 - 준비중)
        """
MSG_START = u'봇 시작.'
MSG_STOP = u'봇 정지.'


class TelegramBot:

    def __init__(self):
        # 토큰 세팅
        self.bot = telegram.Bot(token=TELEGRAM_TOKEN)
        # 변수 선언
        self.msg_id = None
        self.msg_id = None
        self.chat_id = None
        self.text = None

    def send_message_new_list(self):
        # today = datetime.now().date()
        # today = datetime.combine(today, time())
        torrent_movie_list = TorrentMovie.objects.filter(date__gte=datetime.now().date())
        logger.info(torrent_movie_list.query)  # 쿼리 로그 출력
        msg = "오늘 신규 등록된 영화 목록\n"

        if len(torrent_movie_list) > 0:
            for (i, entry) in enumerate(torrent_movie_list):
                # html 유형의 메시지 생성 (텍스트에 링크 추가)
                links = BeautifulSoup(features='html.parser')
                a_tag = links.new_tag('a', href=entry.torrent_detail_url)
                a_tag.string = entry.torrent_movie_name
                # links.append(a_tag)
                # links.append(links.new_tag('br'))
                # logger.info(links.new_tag('br'))
                msg += str(i + 1) + '. ' + str(a_tag) + '\n'
            # logger.info(msg)
            # self.bot.send_message(chat_id="214363528", text=msg)  # TEST (admin)
            telebot_send_list = TelegramBotEnableStatus.objects.filter(enabled=True)
            for entry in telebot_send_list:
                self.bot.send_message(chat_id=entry.chat_id, text=msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    def process_commands(self, msg):

        u"""사용자 메시지를 분석해 봇 명령을 처리
        chat_id: (integer) 채팅 ID
        text:    (string)  사용자가 보낸 메시지 내용
        """
        self.msg_id = msg['message_id']
        self.chat_id = msg['chat']['id']
        self.text = msg['text']
        # logging.info(self.msg_id)
        if not self.text:
            return
        elif BUTTON_START == self.text:
            self.button_start(self.chat_id)
            return
        elif not self.get_enabled(self.chat_id):
            return
        elif BUTTON_STOP == self.text:
            self.button_stop(self.chat_id)
            return
        elif BUTTON_HELP == self.text:
            self.button_help(self.chat_id)
            return
        else:
            self.bot.send_message(chat_id=self.chat_id, text=USAGE + "\n!!명령어를 확인하세요!!")
            # cmd_echo(chat_id, text, reply_to=msg_id)
        return

    def button_start(self, chat_id):
        u"""봇을 활성화하고, 활성화 메시지 발송
        chat_id: (integer) 채팅 ID
        """
        # print("START BUTTON START")
        BUTTON_KEYBOARD = [
            [BUTTON_START],
            [BUTTON_STOP],
            [BUTTON_HELP],
        ]
        reply_markup = json.dumps({
            'keyboard': BUTTON_KEYBOARD,
            'resize_keyboard': True,
            'one_time_keyboard': False,
            # 'selective': (reply_to != None),
        })

        self.set_enabled(chat_id, True)
        self.bot.send_message(chat_id, MSG_START, reply_markup=reply_markup)

    def button_stop(self, chat_id):
        u"""봇을 비활성화하고, 비활성화 메시지 발송
        chat_id: (integer) 채팅 ID
        """
        # print("START BUTTON STOP")
        self.set_enabled(chat_id, False)
        self.bot.send_message(chat_id, MSG_STOP)

    def set_enabled(self, chat_id, enabled):
        u"""봇 활성화/비활성화 상태 변경
        chat_id:    (integer) 봇을 활성화/비활성화할 채팅 ID
        enabled:    (boolean) 지정할 활성화/비활성화 상태
        """
        telebot_enable_status, created = TelegramBotEnableStatus.objects.get_or_create(chat_id=chat_id, defaults={'enabled': enabled})
        if not created:  # 이미 값이 존재 할 경우 업데이트
            telebot_enable_status.enabled = enabled
            telebot_enable_status.save()

    def get_enabled(self, chat_id):
        u"""봇 활성화/비활성화 상태 반환
        return: (boolean)
        """
        telebot_enable_status = TelegramBotEnableStatus.objects.get(chat_id=chat_id)
        if telebot_enable_status:
            return telebot_enable_status.enabled

    def button_help(self, chat_id):
        self.bot.send_message(chat_id=chat_id, text=USAGE)
