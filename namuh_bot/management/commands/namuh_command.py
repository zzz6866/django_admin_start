# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from namuh_bot.simple_http_request_handler import http_server_start


# django 설정 사용 가능 class
# python manage.py namuh_command
class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        http_server_start()
