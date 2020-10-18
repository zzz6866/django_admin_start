# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(StockCd)
class StockCdAdmin(admin.ModelAdmin):
    list_display = ['cd', 'nm']
    list_display_links = ['cd', 'nm']


@admin.register(StockCmdBaseCd)
class StockCmdBaseCdAdmin(admin.ModelAdmin):
    list_display = ['cmd', 'prnt_cmd', 'level', 'required']
    list_display_links = ['cmd', 'prnt_cmd', 'level', 'required']


admin.site.register(StockCmdParam)
