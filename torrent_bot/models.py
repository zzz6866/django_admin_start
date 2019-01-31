import datetime

from django.db import models


# Create your models here.
# 토렌트 영화 수집 모델

class TorrentMovie(models.Model):
    torrent_id = models.BigIntegerField(null=False, unique=True)
    torrent_movie_name = models.CharField(max_length=255)
    torrent_detail_url = models.CharField(max_length=500)
    task_id = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(default=datetime.date.today, blank=False)
