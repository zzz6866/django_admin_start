import numpy as np
import talib

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # tasks.get_public_ticker.delay('ed44b6717266ba4deb8be23ee709f866', '23ed5c220f0ac1eae571ede8c5c9225f')
    # tasks.get_public_ticker('ed44b6717266ba4deb8be23ee709f866', '23ed5c220f0ac1eae571ede8c5c9225f')
    # tasks.expected_indicator()

    import numpy
    import talib

    close = numpy.random.random(50)
    # print(close)

    output = talib.SMA(close)
    print(output)

    return HttpResponse(output)


def index_html(request):
    return render(request, 'index.html', {})
