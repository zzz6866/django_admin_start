from django import forms
from django.forms import PasswordInput

from dal import autocomplete
from django.template import loader
# class SelectOptionAddAttribute(forms.Select):  # select option 태그에 attr 추가 되도록 재정의
#     def __init__(self, attrs=None, choices=(), option_attrs=None):
#         if option_attrs is None:
#             option_attrs = {}
#         self.option_attrs = option_attrs
#         super().__init__(attrs, choices)
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         index = str(index) if subindex is None else "%s_%s" % (index, subindex)
#         if attrs is None:
#             attrs = {}
#         option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
#         if selected:
#             option_attrs.update(self.checked_attribute)
#         if 'id' in option_attrs:
#             option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
#
#         # setting the attributes here for the option
#         if len(self.option_attrs) > 0:
#             if value in self.option_attrs:
#                 custom_attr = self.option_attrs[value]
#                 for k, v in custom_attr.items():
#                     option_attrs.update({k: v})
#
#         return {
#             'name': name,
#             'value': value,
#             'label': label,
#             'selected': selected,
#             'index': index,
#             'attrs': option_attrs,
#             'type': self.input_type,
#             'template_name': self.option_template_name,
#         }
from django.utils.safestring import mark_safe
from nested_admin.nested import NestedTabularInline

from namuh_bot.models import ProcValid, ProcOrder, CD


class ProcValidFormInline(NestedTabularInline):
    model = ProcValid
    # form = ProcDtlValForm
    exclude = ['max_plus_value']
    max_num = 2
    fk_name = 'parent'


# class SelectProcOrder(autocomplete.ModelSelect2):
#     template_name = 'admin/forms/select_proc_order.html'


class ProcOrderForm(forms.ModelForm):
    buy_cd = forms.ModelChoiceField(queryset=CD.objects.all(), widget=autocomplete.ModelSelect2(url='/namuh_bot/cd-autocompleteView/'))


class ProcOrderFormInline(NestedTabularInline):
    model = ProcOrder
    form = ProcOrderForm
    max_num = 1
    fk_name = 'parent'
    inlines = [ProcValidFormInline]
    readonly_fields = ['is_buy']
    exclude = ['order_no']


class ProcLoginForm(forms.ModelForm):
    class Meta:
        widgets = {
            'sz_pw': PasswordInput(render_value=True),
            'sz_cert_pw': PasswordInput(render_value=True),
            'account_pw': PasswordInput(render_value=True),
            'trade_pw': PasswordInput(render_value=True),
        }
