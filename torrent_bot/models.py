import datetime

from django.db import models


# Create your models here.
# 토렌트 영화 수집 모델

class TorrentMovie(models.Model):
    torrent_id = models.BigIntegerField(null=False)
    torrent_movie_name = models.CharField(max_length=100)
    torrent_movie_url = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.date.today, blank=True)
