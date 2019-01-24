from django.conf.urls import url
from coin_bot import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^index_html$', views.index_html),
]
