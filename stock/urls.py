from django.conf.urls import url
from django.urls import path, include

from stock import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list', views.index_html),
    url(r'^test_celery$', views.test_celery),
    url(r'^test_aa$', views.test),
]
