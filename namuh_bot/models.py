# -*- coding: utf-8 -*-
from django.db import models


# 종목코드 모델
class StockCd(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '종목코드'
    # http://kind.krx.co.kr/corpgeneral/corpList.do?method=download (한국 거래소에서 종목 코드 리스트 수집)
    #     opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    cd = models.CharField(max_length=6, primary_key=True, verbose_name='종목코드')
    nm = models.CharField(max_length=100, verbose_name='종목명')


# 명령어 코드 모델
class StockCmdBaseCd(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '명령어 코드'
    cmd = models.CharField(max_length=15, null=False, unique=True, verbose_name='명령어 코드')  # 명령어 코드
    prnt_cmd = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, to_field='cmd', verbose_name='상위 명령어 코드')
    level = models.SmallIntegerField(null=False, verbose_name='단계')  # 명령어 레벨
    required = models.BooleanField(null=True, verbose_name='필수여부')  # 필수여부
    comment = models.TextField(verbose_name='설명')


# 명령어에 대한 변수값 저장
class StockCmdParam(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '명령어 변수'
    base_cmd = models.ForeignKey(StockCmdBaseCd, on_delete=models.CASCADE)  # 명령어 코드
    key = models.CharField(max_length=20, null=False)  # 변수명
    value = models.CharField(max_length=50, null=False)  # 변수 값
