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


# 명령어 코드 모델
class StockCmdBaseCd(MPTTModel):
    class Meta:
        # Add verbose name
        verbose_name_plural = '명령어 코드'

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='상위 명령어 코드')
    name = models.CharField(max_length=15, null=False, verbose_name='명령어')  # 명칭
    cmd = models.CharField(max_length=15, null=False, unique=True, verbose_name='코드')  # 명령어 코드
    comment = models.TextField(verbose_name='설명')

    def __str__(self):
        return self.cmd


class StockOrder(models.Model):
    class Meta:
        verbose_name_plural = '종목 주문 내역'

    stock_cd = models.ForeignKey(StockCd, on_delete=models.CASCADE, to_field='cd', verbose_name='종목코드')
    state = models.BooleanField(default=False, verbose_name='처리상태')  # True : 완료, False : 처리중
    price = models.IntegerField(null=False, verbose_name='구입 단가')  # 구입 단가
    qty = models.IntegerField(null=False, verbose_name='구입 수량')  # 구입 수량
    avg_price = models.IntegerField(null=False, verbose_name='평균 단가')  # 평균 단가


class StockOrderVaild(models.Model):
    class Meta:
        verbose_name_plural = '종목 주문 유효성'

    parent = models.ForeignKey(StockOrder, blank=True, null=True, on_delete=models.CASCADE, verbose_name='상위 주문 번호')
    cd = models.CharField(max_length=20, null=False, verbose_name='구분 코드')  # 금액(amt) or 백분율(per)
    val = models.CharField(max_length=20, null=False, verbose_name='값')  # 값
    time = models.CharField(max_length=2, null=False, verbose_name='오전/오후 구분')  # AM or PM


class StockProc(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=15)  # 명칭


class StockProcDtl(models.Model):
    parent = models.ManyToManyField(StockProc, blank=True, null=True, on_delete=models.CASCADE, verbose_name='상위 번호')
    parent_cmd = models.ForeignKey(StockCmdBaseCd, blank=True, null=True, on_delete=models.CASCADE, verbose_name='상위 명령어')


# 명령어에 대한 변수값 저장
class StockCmdParam(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '명령어 변수'

    parent_cmd = models.ForeignKey(StockCmdBaseCd, on_delete=models.CASCADE, blank=True, null=True, verbose_name='상위 명령어 ID')  # 명령어 ID
    parent_proc = models.ForeignKey(StockProc, on_delete=models.CASCADE, blank=True, null=True, verbose_name='상위 프로세스 ID')  # 프로세스 ID
    val = models.CharField(max_length=50, null=False, verbose_name='value')  # 변수 값
