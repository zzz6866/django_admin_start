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

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in StockCmdBaseCd.objects.filter(prnt_cmd=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

# 명령어에 대한 변수값 저장
class StockCmdParam(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '명령어 변수'

    prnt_cmd = models.ForeignKey(StockCmdBaseCd, on_delete=models.CASCADE, to_field='cmd', verbose_name='명령어 변수')  # 명령어 코드
    val = models.CharField(max_length=50, null=False, verbose_name='변수값')  # 변수 값


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

    prnt_id = models.ForeignKey(StockOrder, on_delete=models.CASCADE, verbose_name='상위 주문 번호')
    cd = models.CharField(max_length=20, null=False, verbose_name='구분 코드')  # 금액(amt) or 백분율(per)
    val = models.CharField(max_length=20, null=False, verbose_name='값')  # 값
    time = models.CharField(max_length=2, null=False, verbose_name='오전/오후 구분')  # AM or PM
