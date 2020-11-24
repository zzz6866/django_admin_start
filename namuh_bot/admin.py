# -*- coding: utf-8 -*-
from nested_inline.admin import *

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


# CHOICES_LEVEL = {
#     'query': {'data-level': '1'},
#     'attach': {'data-level': '2'},
#     'connect': {'data-level': '3'},
#     'disconnect': {'data-level': '4'},
#     # 구분선 (위 req_id , 아래 param)
#     'is_hts': {'data-level': '3'},
#     'sz_id': {'data-level': '3'},
#     'sz_pw': {'data-level': '3'},
#     'sz_cert_pw': {'data-level': '3'},
#     'nInputLen': {'data-level': '1'},
#     'nCodeLen': {'data-level': '1'},
#     'szInput': {'data-level': '1'},
#     'szBCType': {'data-level': '1'},
#     'szTRCode': {'data-level': '1'},
#     'nTRID': {'data-level': '1'},
# }


class ProcValidFormInline(NestedTabularInline):
    model = ProcValid
    # form = ProcDtlValForm
    extra = 1
    fk_name = 'parent'


class ProcOrderFormInline(NestedTabularInline):
    model = ProcOrder
    # form = ProcOrderForm
    extra = 1
    fk_name = 'parent'
    inlines = [ProcValidFormInline]

    # def __str__(self):
    #     return ''


@admin.register(Proc)
class ProcAdmin(NestedModelAdmin):
    list_display = ['name', 'status']
    list_display_links = ['name']
    exclude = ['proc_type']
    inlines = [ProcOrderFormInline]

    class Media:
        js = [
            'forms/js/select_stock_proc.js',
        ]


@admin.register(ProcLogin)
class ProcLoginAdmin(admin.ModelAdmin):
    # def get_model_perms(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
    #     return {}
    def has_module_permission(self, request):  # 모델 리스트에서 제외, proc 상세 뷰에서 추가 및 수정 처리 함
        return False
