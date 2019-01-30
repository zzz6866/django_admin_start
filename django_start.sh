#!/usr/bin/env bash
# conda install -c quantopian ta-lib # anaconda 설치 패턴 conda install -c conda-forge celery
# set DJANGO_SETTINGS_MODULE=alldev.settings.production # Windows shell
export DJANGO_SETTINGS_MODULE=alldev.settings.production # Unix Bash shell

celery -A alldev worker -B -l INFO &
#celery -A alldev beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler & # worker -B 옵션으로 실행하지 않아도 DB 스케쥴 사용
python manage.py runserver 0.0.0.0:8000 &