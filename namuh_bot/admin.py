# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *


# Register your models here.

@admin.register(StockCd)
class StockCdAdmin(admin.ModelAdmin):
    list_display = ['cd', 'nm']
    list_display_links = ['cd', 'nm']


@admin.register(StockCmdBaseCd)
class StockCmdBaseCdAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_name', 'cmd', 'comment']
    list_display_links = ['indented_name']

    def indented_name(self, instance):  # 하위 코드 들여쓰기 재정의
        from django.utils.html import format_html
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.name,  # Or whatever you want to put here
        )

    indented_name.short_description = '명칭'


@admin.register(StockCmdParam)
class StockCmdParamAdmin(admin.ModelAdmin):
    list_display = ['parent_cmd', 'val']
    list_display_links = ['parent_cmd']


@admin.register(StockProc)
class StockProcessAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
