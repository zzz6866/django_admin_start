from django.conf.urls import url
from namuh_bot import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^index_html$', views.index_html),
]
