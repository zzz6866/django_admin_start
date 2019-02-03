from django.conf.urls import url
from django.urls import path

from torrent_bot import views
from torrent_bot.views import WebhookHandler

urlpatterns = [
    url(r'^$', views.index_html),
    # url(r'^webhook$', Webhook.as_view()),
    path('webhook/', WebhookHandler.as_view()),
]
