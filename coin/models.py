from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
# 거래소 마지막 거래 정보
class PublicTicker(models.Model):
    coinCode = models.CharField(max_length=7)
    openingPrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    closingPrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    minPrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    maxPrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    averagePrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    unitsTraded = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0.0)
    volume1Day = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    volume7Day = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    buyPrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    sellPrice = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    dayFluctate = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    dayFluctate_rate = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0.0)
    date = models.DateTimeField

    @classmethod
    def jsonToModel(cls, coinCode=None, json=None, date=None):
        model = cls(coinCode=coinCode,
                    openingPrice=json['opening_price'],
                    closingPrice=json['closing_price'],
                    minPrice=json['min_price'],
                    maxPrice=json['max_price'],
                    averagePrice=json['average_price'],
                    unitsTraded=json['units_traded'],
                    volume1Day=json['volume_1day'],
                    volume7Day=json['volume_7day'],
                    buyPrice=json['buy_price'],
                    sellPrice=json['sell_price'],
                    dayFluctate=json['24H_fluctate'],
                    dayFluctate_rate=json['24H_fluctate_rate'],
                    date=date.strptime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    )
        model.save()
