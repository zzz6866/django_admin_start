import numpy as np
import talib

from django.http import HttpResponse
from django.shortcuts import render

from torrent_bot import tasks


def index_html(request):
    tasks.search_new_video()
    return render(request, 'torrrent/index.html', {})
    # return HttpResponse("aaaa")
