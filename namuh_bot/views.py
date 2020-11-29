# -*- coding: utf-8 -*-
from django.shortcuts import render
from dal import autocomplete

from namuh_bot.models import CD


def index(request):
    return render(request, 'index.html', {})


class CDAutocompleteView(autocomplete.Select2QuerySetView):
    # 종목 코드 ajax 처리를 위한 view 추가 (foreignKey 로 연결 되어 있으나 페이지 로드에 코드 가져올 경우 느리기 때문에 추가)
    def get_queryset(self):
        qs = CD.objects.all()
        if self.q:
            qs = qs.filter(nm__istartswith=self.q)
        return qs
