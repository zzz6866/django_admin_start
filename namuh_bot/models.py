# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# 종목코드 모델
class StockCd(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '종목코드'

    # http://kind.krx.co.kr/corpgeneral/corpList.do?method=download (한국 거래소에서 종목 코드 리스트 수집)
    #     opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    cd = models.CharField(max_length=6, primary_key=True, verbose_name='종목코드')
    nm = models.CharField(max_length=100, verbose_name='종목명')


class StockProc(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=15, verbose_name='이름')  # 명칭
    status = models.BooleanField(default=False, verbose_name='완료 유무')  # 완료 유무


class StockProcDtl(models.Model):
    parent = models.ForeignKey(StockProc, blank=False, default=None, verbose_name='상위 번호', on_delete=models.CASCADE)
    cmd = models.CharField(max_length=15, blank=False, default=None, verbose_name='명령어')
    key = models.CharField(max_length=15, blank=False, default=None, verbose_name='입력키')
    val = models.CharField(max_length=15, blank=False, default=None, verbose_name='입력값')
