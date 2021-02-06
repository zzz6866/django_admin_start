# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import models
from mirage import fields
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


class EncryptedCharFieldNotDecrypt(fields.EncryptedCharField):  # 복호화 방지 class
    def from_db_value(self, value, expression, connection, *args):
        return value


class ProcLogin(models.Model):
    def __str__(self):
        return self.name + ' - ' + self.sz_id

    class Meta:
        # Add verbose name
        verbose_name_plural = '나무 로그인 정보'
        verbose_name = '나무 로그인 정보'

    name = models.CharField(max_length=15, verbose_name='별칭')  # 명칭
    sz_id = models.CharField(max_length=15, verbose_name='로그인 아이디')  # 로그인 ID
    sz_pw = fields.EncryptedCharField(verbose_name='로그인 비밀번호', null=False)  # models.CharField(max_length=15, verbose_name='로그인 PW')  # 로그인 PW
    sz_cert_pw = fields.EncryptedCharField(verbose_name='인증서 비밀번호', null=False)  # models.CharField(max_length=15, verbose_name='인증서 비밀번호')  # 인증서 비밀번호
    account_pw = models.CharField(max_length=44, verbose_name='계좌 비밀번호', null=False)  # 계좌 비밀번호
    trade_pw = models.CharField(max_length=44, verbose_name='거래 비밀번호', null=False)  # 거래 비밀번호
    is_hts = models.BooleanField(default=True, verbose_name='모의투자 여부', null=False)  # 완료 유무

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if self. # TODO 거래비밀번호, 게좌비밀번호 hash 암호화 처리 필요(문의한 내용 답변 받아야 처리 가능)
        super().save(force_insert, force_update, using, update_fields)


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
    login_info = models.ForeignKey(ProcLogin, blank=False, default=None, verbose_name='나무 로그인 정보', on_delete=models.CASCADE)


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
    order_no = models.CharField(max_length=10, verbose_name='체결 주문 번호', null=True)  # 체결 주문 번호


class ProcValid(models.Model):
    def __str__(self):
        return ''

    class Meta:
        # Add verbose name
        verbose_name_plural = '조건식 입력'
        verbose_name = '조건식 입력'
        constraints = [
            models.UniqueConstraint(fields=['parent', 'is_noon'], name="parent-is_noon")  # 조건부 유니크 값 설정 중복 저장 방지
        ]

    parent = models.ForeignKey(ProcOrder, blank=False, default=None, verbose_name='상위 번호', on_delete=models.CASCADE)
    is_noon = models.CharField(max_length=2, verbose_name='오전/오후 구분', choices=(('AM', '오전'), ('PM', '오후')))
    plus_value = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0, verbose_name='익절 값')
    plus_type_code = models.CharField(max_length=2, verbose_name='익절 타입', choices=(('P', '%'), ('W', '원')))
    max_plus_value = models.IntegerField(validators=[RegexValidator(r'^[0-9]+$')], default=0, verbose_name='최종 익절 가격')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # db에 미리 계산 처리 하여 값 비교시 따로 계산하지 않도록 처리(리소스 낭비 방지)
        if self.plus_type_code == 'P':  # 정률
            self.max_plus_value = int(self.parent.buy_price + (self.parent.buy_price * self.plus_value / 100))
        elif self.plus_type_code == 'W':  # 정액
            self.max_plus_value = int(self.plus_value + self.parent.buy_price)

        super().save(force_insert, force_update, using, update_fields)
