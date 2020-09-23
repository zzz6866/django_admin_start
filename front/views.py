from celery.utils.log import get_task_logger
from django.views.generic import TemplateView

logger = get_task_logger(__name__)


class LoginView(TemplateView):
    template_name = "front/login.html"
    title = "로그인 페이지"

    def get(self, request, *args, **kwargs):
        ctx = {
            'title': self.title,
        }
        return self.render_to_response(ctx)
