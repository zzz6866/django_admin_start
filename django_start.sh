#!/usr/bin/env bash
# set DJANGO_SETTINGS_MODULE=coin_bot.settings.local #  Windows shell
export DJANGO_SETTINGS_MODULE=coin_bot.settings.local # Unix Bash shell

celery -A coin_bot worker -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
celery -A coin_bot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
python manage.py runserver 192.168.0.2:8000 --settings=coin_bot.settings.production &