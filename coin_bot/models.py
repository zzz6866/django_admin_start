import datetime

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
# 거래소 마지막 거래 정보
from django.utils import timezone


class PublicTicker(models.Model):
    coin_code = models.CharField(max_length=7)
    opening_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    closing_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    min_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    max_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    average_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    units_traded = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0.0)
    volume_1day = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    volume_7day = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    buy_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    sell_price = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    day_fluctate = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0)
    day_fluctate_rate = models.FloatField(validators=[RegexValidator(r'^[0-9]+\.?[0-9]+$')], default=0.0)
    date = models.DateTimeField(null=True, blank=True)

    @classmethod
    def set_json(cls, coin_code=None, json=None, date=None):
        # datetime.fromtimestamp(1350663248, tz= pytz.timezone('America/New_York'))
        timestamp = datetime.datetime.fromtimestamp(float(date) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        # localtz = pytz.timezone(settings.TIME_ZONE)
        # timestamp = localtz.localize(timestamp)
        timestamp = timezone.make_aware(timestamp)
        # print(timestamp)
        # print(coinCode)

        model = cls(coin_code=coin_code,
                    opening_price=json['opening_price'],
                    closing_price=json['closing_price'],
                    min_price=json['min_price'],
                    max_price=json['max_price'],
                    average_price=json['average_price'],
                    units_traded=json['units_traded'],
                    volume_1day=json['volume_1day'],
                    volume_7day=json['volume_7day'],
                    buy_price=json['buy_price'],
                    sell_price=json['sell_price'],
                    day_fluctate=json['24H_fluctate'],
                    day_fluctate_rate=json['24H_fluctate_rate'],
                    date=timestamp,
                    )
        model.save()

    # def __str__(self):
    #     return super().__str__()
