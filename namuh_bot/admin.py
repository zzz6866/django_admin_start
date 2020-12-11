# -*- coding: utf-8 -*-
from django.contrib import admin
from nested_admin.nested import NestedModelAdmin

from .forms import *
from .models import *


# Register your models here.

@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['cd', 'nm']
    list_display_links = ['cd', 'nm']

    def get_model_perms(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
        return {'view': self.has_view_permission(request)}

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Proc)
class ProcAdmin(NestedModelAdmin):
    list_display = ['name', 'status']
    list_display_links = ['name']
    exclude = ['proc_type']
    inlines = [ProcOrderFormInline]


@admin.register(ProcLogin)
class ProcLoginAdmin(admin.ModelAdmin):
    # def get_model_perms(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
    #     return {}
    form = ProcLoginForm

    def has_module_permission(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
        return False
