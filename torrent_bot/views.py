import json

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from torrent_bot.telegram_bot import TelegramBot


@method_decorator(csrf_exempt, name='dispatch')
class WebhookHandler(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        json_body = json.loads(request.body.decode("utf-8"))
        # process_cmds(json_body['message'])
        return JsonResponse(json_body)


def index_html(request):
    # bot = TelegramBot()
    # bot.send_message_new_list()
    # tasks.find_new_torrent_movie()

    telegrambot = TelegramBot()
    # telegrambot.bot.delete_webhook()
    updates = telegrambot.bot.getUpdates()
    for u in updates:
        # print(u.message)
        telegrambot.process_commands(u.message)

    return render(request, 'torrrent/index.html', {"updates": updates})
