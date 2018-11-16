# Generated by Django 2.1.3 on 2018-11-14 13:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicTicker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinCode', models.CharField(max_length=7)),
                ('openingPrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('closingPrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('minPrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('maxPrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('averagePrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('unitsTraded', models.FloatField(max_length=15)),
                ('volume1Day', models.FloatField(max_length=15)),
                ('volume7Day', models.FloatField(max_length=15)),
                ('buyPrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('sellPrice', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('dayFluctate', models.IntegerField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('dayFluctate_rate', models.FloatField(max_length=10)),
            ],
        ),
    ]
