from datetime import datetime, time

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from torrent_bot.models import TorrentMovie, TelegramBotEnableStatus

TELEGRAM_TOKEN = '763953984:AAHZYhC_K5g8c11skZglFdohl6j9JX2t6Hs'

# 봇이 응답할 명령어
BUTTON_START = '/start'
BUTTON_STOP = '/stop'
sBUTTON_NEW_LIST_TORRNET = '/button_new_list_torrnet'
BUTTON_FIND_TORRNET = '/button_find_torrnet'

# 봇 사용법 & 메시지
USAGE = u"""[사용법] 아래 명령어를 메시지로 보내거나 버튼을 누르시면 됩니다.
        /start - (봇 활성화)
        /stop  - (봇 비활성화)
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
        print(torrent_movie_list.query)
        msg = "신규 등로된 영화 목록\n"

        for (i, entry) in enumerate(torrent_movie_list):
            msg += str(i + 1) + '. ' + entry.torrent_movie_name + "\n"
        print(msg)
        # self.bot.send_message(chat_id="214363528", text=msg)
        self.bot.send_message(chat_id="214363528", text=msg)

    def process_commands(self, msg):

        u"""사용자 메시지를 분석해 봇 명령을 처리
        chat_id: (integer) 채팅 ID
        text:    (string)  사용자가 보낸 메시지 내용
        """
        self.msg_id = msg.message_id
        self.chat_id = msg.chat.id
        self.text = msg.text
        print(self.msg_id, self.text)
        if not self.text:
            return
        if BUTTON_START == self.text:
            self.button_start(self.chat_id)
            return
        if not self.get_enabled(self.chat_id):
            return
        if BUTTON_STOP == self.text:
            self.button_stop(self.chat_id)
            return
        # if CMD_HELP == text:
        #     cmd_help(chat_id)
        #     return
        # cmd_broadcast_match = re.match('^' + CMD_BROADCAST + ' (.*)', text)
        # if cmd_broadcast_match:
        #     cmd_broadcast(chat_id, cmd_broadcast_match.group(1))
        #     return
        # cmd_echo(chat_id, text, reply_to=msg_id)
        return

    def button_start(self, chat_id):
        u"""cmd_start: 봇을 활성화하고, 활성화 메시지 발송
        chat_id: (integer) 채팅 ID
        """
        # print("START BUTTON START")
        BUTTON_KEYBOARD = [
            [BUTTON_START],
            [BUTTON_STOP]
        ]
        self.set_enabled(chat_id, True)
        self.bot.send_message(chat_id, MSG_START, keyboard=BUTTON_KEYBOARD)

    def button_stop(self, chat_id):
        u"""cmd_stop: 봇을 비활성화하고, 비활성화 메시지 발송
        chat_id: (integer) 채팅 ID
        """
        # print("START BUTTON STOP")
        self.set_enabled(chat_id, False)
        self.bot.send_message(chat_id, MSG_STOP, keyboard=None)

    def set_enabled(self, chat_id, enabled):
        u"""set_enabled: 봇 활성화/비활성화 상태 변경
        chat_id:    (integer) 봇을 활성화/비활성화할 채팅 ID
        enabled:    (boolean) 지정할 활성화/비활성화 상태
        """
        telebot_enable_status = TelegramBotEnableStatus.objects.get_or_create(chat_id=str(chat_id), defaults={'enabled': enabled})
        # telebot_enable_status.enabled = enabled
        # telebot_enable_status.save()

    def get_enabled(self, chat_id):
        u"""get_enabled: 봇 활성화/비활성화 상태 반환
        return: (boolean)
        """
        telebot_enable_status = TelegramBotEnableStatus.objects.get(chat_id=str(chat_id))
        if telebot_enable_status:
            return telebot_enable_status.enabled
