from django.conf.urls import url
from torrent_bot import views

urlpatterns = [
    url(r'^$', views.index_html),
]
