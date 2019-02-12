import json
from datetime import datetime

import telegram
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
from telegram import ParseMode, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton

from torrent_bot.models import TorrentMovie, TelegramBotEnableStatus
from torrent_bot.selenium_chrome import SeleniumChrome

logger = get_task_logger(__name__)

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '763953984:AAHZYhC_K5g8c11skZglFdohl6j9JX2t6Hs'

# 봇이 응답할 명령어
BUTTON_START = '/start'
BUTTON_STOP = '/stop'
BUTTON_HELP = '/help'
BUTTON_NEW_LIST_TORRNET = '/new_list_torrent'
BUTTON_FIND_TORRNET = '/find_torrent'
BUTTON_FIND_TORRNET2 = '/find_torrent2'

# 봇 사용법 & 메시지
USAGE_HELP = u"""[사용법] 아래 명령어를 메시지로 보내거나 버튼을 누르시면 됩니다.
        /start - (봇 활성화)
        /stop  - (봇 비활성화)
        /help  - (도움말)
        /button_new_list_torrnet  - (신규 토렌트 영화 목록)
        /button_find_torrnet  - (토렌트 검색 - 준비중)
        """
MSG_START = u'봇 시작.'
MSG_STOP = u'봇 정지.'
MSG_FIND_TEXT = u'검색어를 입력하세요.'


class TelegramBot:

    def __init__(self):
        # 토큰 세팅
        self.bot = telegram.Bot(token=TELEGRAM_TOKEN)
        # 변수 선언
        self.msg_id = None
        self.msg_id = None
        self.chat_id = None
        self.text = None

    def send_message_new_list(self, res_list):
        # today = datetime.now().date()
        # today = datetime.combine(today, time())
        # torrent_movie_list = TorrentMovie.objects.filter(date__gte=datetime.now().date())
        # print(torrent_movie_list.query)  # 쿼리 로그 출력
        msg = "🎬오늘 신규 등록된 영화 목록🎬"

        inline_keyboard_list, reply_markup = self.get_inline_keyboard_list(res_list)

        # self.bot.send_message(chat_id="214363528", text=msg)  # TEST (admin)
        if len(inline_keyboard_list) > 0:
            telebot_send_list = TelegramBotEnableStatus.objects.filter(enabled=True)
            for entry in telebot_send_list:
                self.bot.send_message(chat_id=entry.chat_id, text=msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=reply_markup)

    def process_commands(self, msg):

        u"""사용자 메시지를 분석해 봇 명령을 처리
        chat_id: (integer) 채팅 ID
        text:    (string)  사용자가 보낸 메시지 내용
        """
        self.msg_id = msg['message_id']
        self.chat_id = msg['chat']['id']
        self.text = msg['text']
        # logging.info(self.msg_id)
        # print(json.dumps(msg))
        if not self.text:
            return
        elif BUTTON_START == self.text:
            self.cmd_start()
            return
        elif not self.get_enabled():
            return
        elif BUTTON_STOP == self.text:
            self.cmd_stop()
            return
        elif BUTTON_HELP == self.text:
            self.cmd_help()
            return
        elif BUTTON_FIND_TORRNET == self.text:
            # self.cmd_find_torrent(msg['text'])
            # Update Feature with Inline Keyboard
            # promo_keyboard = InlineKeyboardButton(text="Update!", callback_data="update_taxi")
            # custom_keyboard = [[promo_keyboard]]
            # reply_markup = InlineKeyboardMarkup(custom_keyboard)
            # self.bot.send_message(chat_id=self.chat_id, text="input find torrent text1122", reply_markup=reply_markup)
            self.bot.send_message(chat_id=self.chat_id, text=MSG_FIND_TEXT, reply_markup=ForceReply(force_reply=True, selective=False))
            # reply_keyboard = [[telegram.KeyboardButton(text='/1')], [telegram.KeyboardButton(text='/2')]]
            # self.bot.send_message(chat_id=self.chat_id, text="input find torrent text", reply_markup=telegram.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return
            # 토렌트 검색시
        elif MSG_FIND_TEXT in str(msg):
            self.cmd_find_torrent(msg['text'])
            return
        else:
            self.bot.send_message(chat_id=self.chat_id, text=USAGE_HELP + "\n!!명령어를 확인하세요!!")
            # cmd_echo(chat_id, text, reply_to=msg_id)
        return

    def cmd_start(self):
        u"""봇을 활성화하고, 활성화 메시지 발송
        chat_id: (integer) 채팅 ID
        """
        # print("START BUTTON START")
        # BUTTON_KEYBOARD = [
        #     [BUTTON_START],
        #     [BUTTON_STOP],
        #     [BUTTON_HELP],
        # ]
        # reply_markup = json.dumps({
        #     'keyboard': BUTTON_KEYBOARD,
        #     'resize_keyboard': True,
        #     'one_time_keyboard': False,
        #     'selective': (reply_to != None),
        # })

        self.set_enabled(True)
        self.bot.send_message(self.chat_id, MSG_START)

    def cmd_stop(self):
        u"""봇을 비활성화하고, 비활성화 메시지 발송
        chat_id: (integer) 채팅 ID
        """
        # print("START BUTTON STOP")
        self.set_enabled(False)
        self.bot.send_message(self.chat_id, MSG_STOP)

    def set_enabled(self, enabled):
        u"""봇 활성화/비활성화 상태 변경
        chat_id:    (integer) 봇을 활성화/비활성화할 채팅 ID
        enabled:    (boolean) 지정할 활성화/비활성화 상태
        """
        telebot_enable_status, created = TelegramBotEnableStatus.objects.get_or_create(chat_id=self.chat_id, defaults={'enabled': enabled})
        if not created:  # 이미 값이 존재 할 경우 업데이트
            telebot_enable_status.enabled = enabled
            telebot_enable_status.save()

    def get_enabled(self):
        u"""봇 활성화/비활성화 상태 반환
        return: (boolean)
        """
        telebot_enable_status = TelegramBotEnableStatus.objects.get(chat_id=self.chat_id)
        if telebot_enable_status:
            return telebot_enable_status.enabled

    def cmd_help(self):
        """
        도움말
        :return:
        """
        self.bot.send_message(chat_id=self.chat_id, text=USAGE_HELP)

    def cmd_find_torrent(self, find_text):
        """
        토렌트 검색
        :param find_text: 검색어
        :return:
        """
        self.bot.send_message(chat_id=self.chat_id, text="검색중입니다...")
        res_list = SeleniumChrome().get_find_torrent(find_text=find_text)
        # self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        inline_keyboard_list, reply_markup = self.get_inline_keyboard_list(res_list)
        if len(inline_keyboard_list) > 0:
            msg = "검색 결과입니다."
        else:
            msg = "검색된 결과가 없습니다.\n다시 시도하시려면 " + BUTTON_FIND_TORRNET + " 명령어를 입력하세요."

        self.bot.send_message(chat_id=self.chat_id, text=msg, reply_markup=reply_markup)

    def get_inline_keyboard_list(self, res_list):
        inline_keyboard_list = []
        if len(res_list) > 0:
            for i in res_list:
                keyboard = [InlineKeyboardButton(text=i['torrent_title'], callback_data=i['torrent_detail_url'])]
                inline_keyboard_list.append(keyboard)
        reply_markup = InlineKeyboardMarkup(inline_keyboard_list)
        return inline_keyboard_list, reply_markup
