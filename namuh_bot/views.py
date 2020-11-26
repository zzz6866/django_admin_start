# -*- coding: utf-8 -*-
from django.shortcuts import render
from dal import autocomplete

from namuh_bot.models import CD


def index(request):
    return render(request, 'index.html', {})


class CDAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CD.objects.all()
        if self.q:
            qs = qs.filter(nm__istartswith=self.q)
        return qs
