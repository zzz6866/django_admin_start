import win32gui
from django.core.management.base import BaseCommand
from django.utils import timezone

from namuh_bot.namuh_windows import NamuhWindow


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        w = NamuhWindow()
        win32gui.PumpMessages()  # MFC 메시지 수집
