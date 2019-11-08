from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
# 단타 도우미 models
from django.utils import timezone


class FlipperHelper(models.Model):
    investmentable_amount = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)  # 투자 가능 금액(증권사 입금 금액)
    investment_amount = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)  # 투자 시점 금액
    min_limit_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 총 손절 마지노선 (%)
    max_limit_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 총 익절 마지노선 (%)
    investment_now_amount = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)  # 투자 후 현재 금액(변동)
    min_limit_now_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 투자 후 현재 금액(변동)의 손절 마지노선 (%)
    max_limit_now_percent = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')])  # 투자 후 현재 금액(변동)의 익절 마지노선 (%)
