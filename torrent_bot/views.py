import numpy as np
import talib

from django.http import HttpResponse
from django.shortcuts import render

from torrent_bot import tasks


def index_html(request):
    page_source = tasks.find_new_torrent()
    return render(request, 'torrrent/index.html', {"page_source": page_source})
    # return HttpResponse("aaaa")
