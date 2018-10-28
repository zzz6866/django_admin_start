from django.http import HttpResponse
from django.shortcuts import render
from stock import tasks


def index(request):
    return HttpResponse("Hello, world. You're at the index.11111111111")


def index_html(request):
    return render(request, 'stock/index.html', {})


def test_celery(request):
    # result = tasks.sleeptask.delay(2)
    result2 = tasks.add.delay(2, 5)
    result2.ready()
    return HttpResponse("this is task test (id : %s, value : %d)" % (result2, result2.get()))


def test(request):
    result = tasks.add.delay(2, 5)
    print(result.state)
    return HttpResponse(result)
