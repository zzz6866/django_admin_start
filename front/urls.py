# -*- coding: utf-8 -*-
from django.conf.urls import url
from front import views

urlpatterns = [
    url(r'login/$', views.LoginView.as_view()),
]
