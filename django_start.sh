#!/usr/bin/env bash
# conda install -c quantopian ta-lib # anaconda 설치 패턴 conda install -c conda-forge celery
# set DJANGO_SETTINGS_MODULE=alldev.settings.production # Windows shell
# export DJANGO_SETTINGS_MODULE=alldev.settings.production # Unix Bash shell

# celery -A alldev worker -B -l INFO  # 로컬 개발 환경 실행
# django running
if [[ *"local"* == "$DJANGO_SETTINGS_MODULE" ]]; then
    python manage.py runserver 0.0.0.0:8000 & # django run
    # brew  # redis start
    nohup celery -A alldev worker -B -l INFO &
    sleep 10
    curl -X GET https://local.alldev.co.kr:8443/torrent/setWebhook/
else
    nohup python manage.py runserver 0.0.0.0:8000 & # django run
    /etc/init.d/redis-server restart # redis start
    service celeryd restart # 데몬 실행
    sleep 10
    curl -X GET https://www.alldev.co.kr:8443/torrent/setWebhook/
fi