# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import models
from mptt.models import MPTTModel


# 종목코드 모델
class CD(models.Model):
    def __str__(self):
        return self.nm + '(' + self.cd + ')'

    class Meta:
        # Add verbose name
        verbose_name_plural = '종목코드'

    # http://kind.krx.co.kr/corpgeneral/corpList.do?method=download (한국 거래소에서 종목 코드 리스트 수집)
    #     opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    cd = models.CharField(max_length=6, primary_key=True, verbose_name='종목코드')
    nm = models.CharField(max_length=100, verbose_name='종목명')


class ProcLogin(models.Model):
    def __str__(self):
        return self.name + ' - ' + self.sz_id

    class Meta:
        # Add verbose name
        verbose_name_plural = '로그인 정보'
        verbose_name = '로그인 정보'

    name = models.CharField(max_length=15, verbose_name='별칭')  # 명칭
    sz_id = models.CharField(max_length=15, verbose_name='로그인 ID')  # 로그인 ID
    sz_pw = models.CharField(max_length=15, verbose_name='로그인 PW')  # 로그인 PW
    sz_cert_pw = models.CharField(max_length=15, verbose_name='인증서 PW')  # 인증서 PW
    is_hts = models.BooleanField(default=True, verbose_name='모의투자 여부')  # 완료 유무


PROC_TYPE_KEY = (
    ('', '-------'),
    ('A', '종목 조회'),
    ('B', '체결 및 모니터링'),
)


class Proc(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        # Add verbose name
        verbose_name_plural = '종목 체결 정보'
        verbose_name = '종목 체결 정보'

    name = models.CharField(max_length=15, verbose_name='이름')  # 명칭
    type_code = models.CharField(max_length=1, verbose_name='요청 구분', blank=True, choices=PROC_TYPE_KEY, default='B')  #
    status = models.BooleanField(default=False, verbose_name='완료 유무')  # 완료 유무
    login_info = models.ForeignKey(ProcLogin, blank=False, default=None, verbose_name='로그인 정보', on_delete=models.CASCADE)


class ProcOrder(models.Model):
    def __str__(self):
        return ''

    class Meta:
        # Add verbose name
        verbose_name_plural = '체결 정보 입력'
        verbose_name = '체결 정보 입력'

    parent = models.ForeignKey(Proc, blank=False, default=None, verbose_name='상위 번호', on_delete=models.CASCADE)
    buy_cd = models.ForeignKey(CD, blank=False, default=None, verbose_name='종목명', on_delete=models.CASCADE)
    buy_price = models.IntegerField(default=0, verbose_name='구매 단가', validators=[RegexValidator(r'^[0-9]+$')])  # 구매 단가
    buy_qty = models.IntegerField(default=0, verbose_name='구매 수량', validators=[RegexValidator(r'^[0-9]+$')])  # 구매 수량
    is_buy = models.BooleanField(default=False, verbose_name='체결 유무')  # 체결 유무(재구매 방지)


class ProcValid(models.Model):
    def __str__(self):
        return ''

    class Meta:
        # Add verbose name
        verbose_name_plural = '조건식 입력'
        verbose_name = '조건식 입력'

    parent = models.ForeignKey(ProcOrder, blank=False, default=None, verbose_name='상위 번호', on_delete=models.CASCADE)
    is_noon = models.CharField(max_length=2, verbose_name='오전/오후 구분', choices=(('AM', '오전'), ('PM', '오후')))
    limit_value = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0, verbose_name='익절 값')
    limit_type_code = models.CharField(max_length=2, verbose_name='익절 타입', choices=(('P', '%'), ('W', '원')))
