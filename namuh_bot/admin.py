# -*- coding: utf-8 -*-
from dal import autocomplete
from django import forms
from django.contrib import admin
from django.forms import PasswordInput
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

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


class SelectOptionAddAttribute(forms.Select):  # select option 태그에 attr 추가 되도록 재정의
    def __init__(self, attrs=None, choices=(), option_attrs=None):
        if option_attrs is None:
            option_attrs = {}
        self.option_attrs = option_attrs
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        # setting the attributes here for the option
        if len(self.option_attrs) > 0:
            if value in self.option_attrs:
                custom_attr = self.option_attrs[value]
                for k, v in custom_attr.items():
                    option_attrs.update({k: v})

        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }


class ProcValidFormInline(NestedTabularInline):
    model = ProcValid
    # form = ProcDtlValForm
    max_num = 2
    fk_name = 'parent'


class ProcOrderForm(forms.ModelForm):
    buy_cd = forms.ModelChoiceField(queryset=CD.objects.all(), widget=autocomplete.ModelSelect2(url='/namuh_bot/cd-autocompleteView/'))


class ProcOrderFormInline(NestedTabularInline):
    model = ProcOrder
    form = ProcOrderForm
    max_num = 1
    fk_name = 'parent'
    inlines = [ProcValidFormInline]


@admin.register(Proc)
class ProcAdmin(NestedModelAdmin):
    list_display = ['name', 'status']
    list_display_links = ['name']
    exclude = ['proc_type']
    inlines = [ProcOrderFormInline]


class ProcLoginForm(forms.ModelForm):
    class Meta:
        widgets = {
            'sz_pw': PasswordInput(render_value=True),
            'sz_cert_pw': PasswordInput(render_value=True),
            'account_pw': PasswordInput(render_value=True),
        }


@admin.register(ProcLogin)
class ProcLoginAdmin(admin.ModelAdmin):
    # def get_model_perms(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
    #     return {}
    form = ProcLoginForm

    def has_module_permission(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
        return False
