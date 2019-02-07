import json

from celery.utils.log import get_task_logger
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from torrent_bot.telegram_bot import TelegramBot

logger = get_task_logger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class WebhookHandler(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body.decode("utf-8"))
        # print(json_body)
        telegrambot = TelegramBot()
        telegrambot.process_commands(json_body['message'])
        return JsonResponse(json_body)


def index_html(request):
    # bot = TelegramBot()
    # bot.send_message_new_list()
    # tasks.find_new_torrent_movie()

    # telegrambot = TelegramBot()
    # telegrambot.bot.delete_webhook()
    # updates = telegrambot.bot.getUpdates()
    # for u in updates:
    #     print(u.message)
    # telegrambot.process_commands(u.message)
    #
    # return render(request, 'torrrent/index.html', {"updates": updates})
    # logger.info('Test log INFO')
    # logger.warning('Test log WARNING')
    # logger.error('Test log ERROR')

    # 텔레그램을 통한 수집된 토렌트에 대한 메시지 밣송
    bot = TelegramBot()
    bot.send_message_new_list()
    return HttpResponse("asdasdasd")
