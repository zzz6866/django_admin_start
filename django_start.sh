#!/usr/bin/env bash
# set DJANGO_SETTINGS_MODULE=alldev.settings.production # Windows shell
export DJANGO_SETTINGS_MODULE=alldev.settings.production # Unix Bash shell

celery -A coin_bot worker -B -l INFO &
#celery -A coin_bot beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler & # worker -B 옵션으로 실행하지 않아도 DB 스케쥴 사용
python manage.py runserver 192.168.0.2:8000 &