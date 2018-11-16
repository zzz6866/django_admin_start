from django.core import serializers
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
    date = models.DateField

    @classmethod
    def jsonToModel(cls, coinCode=None, json=None):
        cls(coinCode=coinCode)
        cls.create()
