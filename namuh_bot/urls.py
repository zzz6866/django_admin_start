# -*- coding: utf-8 -*-
from django.conf.urls import url
from namuh_bot import views
from namuh_bot.views import CDAutocompleteView, StockInfoView

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^cd-autocompleteView/$', CDAutocompleteView.as_view(), name='CD-AutocompleteView'),
    url(r'^getStockinfoView/$', StockInfoView.as_view(), name='StockInfoView'),
]
