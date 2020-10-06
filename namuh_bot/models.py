from django.db import models


# 종목코드 모델
class StockCd(models.Model):
    # http://kind.krx.co.kr/corpgeneral/corpList.do?method=download (한국 거래소에서 종목 코드 리스트 수집)
    #     opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    cd = models.CharField(max_length=6, primary_key=True)
    nm = models.CharField(max_length=100)
