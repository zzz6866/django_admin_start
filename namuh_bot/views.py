# -*- coding: utf-8 -*-

from celery.utils.log import get_task_logger
from dal import autocomplete
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from namuh_bot.models import CD, ProcLogin
from namuh_bot.tasks import request_bot, create_namuh_bot_connect, create_namuh_bot_query

logger = get_task_logger(__name__)


def index(request):
    return render(request, 'index.html', {})


class CDAutocompleteView(autocomplete.Select2QuerySetView):
    # 종목 코드 ajax 처리를 위한 view 추가 (foreignKey 로 연결 되어 있으나 페이지 로드에 코드 가져올 경우 느리기 때문에 추가)
    def get_queryset(self):
        qs = CD.objects.all()
        if self.q:
            qs = qs.filter(nm__istartswith=self.q)
        return qs


class StockInfoView(TemplateView):
    template_name = "admin/change_list.html"
    title = "메인 페이지"

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseNotFound()

    def get(self, request, *args, **kwargs):
        login_info = ProcLogin.objects.get(id=request.GET.get('login_id'))
        param = [
            create_namuh_bot_connect(param=model_to_dict(login_info, exclude=['id', 'name'])),  # 로그인 정보 req
            create_namuh_bot_query(tr_code='c1101', str_input='K\x00' + str(request.GET.get('buy_cd')) + '\x00', len_input=8)  # 종목 정보 req
        ]
        response = request_bot(param)
        # logger.debug(response)
        if any('c1101OutBlock' in d for d in response.json()):
            json_out_block = response.json().get('c1101OutBlock')[0]
            # logger.debug(json_out_block)
        else:
            json_out_block = response.json()

        # ctx = {
        #     'title': self.title,
        # }
        # return self.render_to_response(ctx)
        return JsonResponse(json_out_block, json_dumps_params={'ensure_ascii': True})  # TODO : 템플릿 적용필요
