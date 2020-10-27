# -*- coding: utf-8 -*-
from nested_inline.admin import *

from .models import *


# Register your models here.

@admin.register(StockCd)
class StockCdAdmin(admin.ModelAdmin):
    list_display = ['cd', 'nm']
    list_display_links = ['cd', 'nm']


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


CHOICES_LEVEL = {
    'query': {'data-level': '1'},
    'attach': {'data-level': '2'},
    'connect': {'data-level': '3'},
    'disconnect': {'data-level': '4'},
    # 구분선 (위 cmd , 아래 param)
    'is_hts': {'data-level': '3'},
    'sz_id': {'data-level': '3'},
    'sz_pw': {'data-level': '3'},
    'sz_cert_pw': {'data-level': '3'},
    'nInputLen': {'data-level': '1'},
    'nCodeLen': {'data-level': '1'},
    'szInput': {'data-level': '1'},
    'szBCType': {'data-level': '1'},
    'szTRCode': {'data-level': '1'},
    'nTRID': {'data-level': '1'},
}


class StockProcDtlForm(forms.ModelForm):
    CHOICES_CMD = (
        ('', '-------'),
        ('query', '일회성 조회'),
        ('attach', '실시간 조회'),
        ('connect', '로그인'),
        ('disconnect', '로그아웃'),
    )

    cmd = forms.ChoiceField(choices=CHOICES_CMD, required=True, widget=SelectOptionAddAttribute(option_attrs=CHOICES_LEVEL))


class StockProcDtlValForm(forms.ModelForm):
    CHOICES_KEY = (
        ('', '-------'),
        ('is_hts', '모의투자 여부'),
        ('sz_id', '아이디'),
        ('sz_pw', '비밀번호'),
        ('sz_cert_pw', '인증서 비밀번호'),
        ('nInputLen', '입력값 길이'),
        ('nCodeLen', '입력 코드길이'),
        ('szInput', '입력값'),
        ('szBCType', '조회 타입'),
        ('szTRCode', '조회 항목'),
        ('nTRID', '서비스ID'),
    )
    key = forms.ChoiceField(choices=CHOICES_KEY, required=True, widget=SelectOptionAddAttribute(option_attrs=CHOICES_LEVEL))
    val = forms.CharField(required=True)


class StockProcDtlValFormInline(NestedTabularInline):
    model = StockProcDtlVal
    form = StockProcDtlValForm
    extra = 1
    fk_name = 'parent'


class StockProcDtlFormInline(NestedTabularInline):
    model = StockProcDtl
    form = StockProcDtlForm
    extra = 1
    fk_name = 'parent'
    inlines = [StockProcDtlValFormInline]

    def __str__(self):
        return '명령어 입력'


@admin.register(StockProc)
class StockProcAdmin(NestedModelAdmin):
    list_display = ['name', 'status']
    list_display_links = ['name', 'status']
    inlines = [StockProcDtlFormInline]

    class Media:
        js = [
            'forms/js/select_stock_cmd.js',
        ]
