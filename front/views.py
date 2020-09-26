from celery.utils.log import get_task_logger
from django.views.generic import TemplateView

from namuh_bot.tasks import get_stock_cd_list

logger = get_task_logger(__name__)


class IndexView(TemplateView):
    template_name = "front/index.html"
    title = "메인 페이지"

    def get(self, request, *args, **kwargs):
        ctx = {
            'title': self.title,
        }
        return self.render_to_response(ctx)


class LoginView(TemplateView):
    template_name = "front/login.html"
    title = "로그인 페이지"

    def get(self, request, *args, **kwargs):
        ctx = {
            'title': self.title,
        }
        return self.render_to_response(ctx)
