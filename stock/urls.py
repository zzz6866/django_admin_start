from django.conf.urls import url
from stock import views

urlpatterns = [
    url(r'^index', views.index),
    url(r'^list', views.index_html),
]
