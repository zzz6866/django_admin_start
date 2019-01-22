from django.http import HttpResponse
from django.shortcuts import render

from coin import tasks


def index(request):
    # tasks.get_public_ticker.delay('ed44b6717266ba4deb8be23ee709f866', '23ed5c220f0ac1eae571ede8c5c9225f')
    # tasks.get_public_ticker('ed44b6717266ba4deb8be23ee709f866', '23ed5c220f0ac1eae571ede8c5c9225f')
    return HttpResponse("aaaaaaaaaaaaa")


def index_html(request):
    return render(request, 'index.html', {})
