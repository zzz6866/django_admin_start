# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
# 토렌트 영화 수집 모델

class TorrentMovie(models.Model):
    class Meta:
        # Add verbose name
        verbose_name_plural = '영화 다운로드 내역'
        verbose_name = '영화 다운로드 내역'
    torrent_id = models.BigIntegerField(null=False, unique=True)
    torrent_movie_name = models.CharField(max_length=255)
    torrent_detail_url = models.CharField(max_length=500)
    task_id = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now=True)
    download_yn = models.BooleanField(default=False)


# 사용자별 봇 활성화 상태
# 사용자가 /start 누르면 활성화
# 사용자가 /stop  누르면 비활성화
class TelegramBotEnableStatus(models.Model):
    chat_id = models.BigIntegerField(null=False, unique=True)
    enabled = models.BooleanField(default=False)
