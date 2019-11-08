"""alldev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.static import serve

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # admin css 등 DEBUG = False 설정시 못가져오는 파일들 셋팅
    url(r'^$', lambda r: HttpResponseRedirect('admin/')),
    url(r'^admin/', admin.site.urls),
    # url(r'^coin/', include('coin_bot.urls')), # 미사용 주석처리
    url(r'^torrent/', include('torrent_bot.urls')),
]
