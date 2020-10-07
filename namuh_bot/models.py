from django.db import models


# 종목코드 모델
class StockCd(models.Model):
    # http://kind.krx.co.kr/corpgeneral/corpList.do?method=download (한국 거래소에서 종목 코드 리스트 수집)
    #     opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    cd = models.CharField(max_length=6, primary_key=True)
    nm = models.CharField(max_length=100)


# 명령어 코드 모델
class StockStrategyBaseCd(models.Model):
    cmd = models.CharField(max_length=6, null=False)  # 명령어 코드
    prnt_cmd = models.ForeignKey('self', on_delete=models.SET_NULL)
    level = models.SmallIntegerField(null=False)  # 명령어 레벨
    required = models.BooleanField(null=True)  # 필수여부
    comment = models.TextField()


# 명령어에 대한 변수값 저장
class StockStrategyParam(models.Model):
    base_cmd = models.ForeignKey(StockStrategyBaseCd.cmd, on_delete=models.CASCADE)  # 명령어 코드
    key = models.CharField(max_length=20, null=False)  # 변수명
    value = models.CharField(max_length=50, null=False)  # 변수 값
