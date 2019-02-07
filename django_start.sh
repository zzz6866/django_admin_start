#!/usr/bin/env bash
# conda install -c quantopian ta-lib # anaconda 설치 패턴 conda install -c conda-forge celery
# set DJANGO_SETTINGS_MODULE=alldev.settings.production # Windows shell
export DJANGO_SETTINGS_MODULE=alldev.settings.production # Unix Bash shell

# celery -A alldev worker -B -l INFO  # 로컬 개발 환경 실행
service celeryd restart # 데몬 실행
python manage.py runserver 0.0.0.0:8000