from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# set today
today = datetime.today().date()

# scheduler configuration
app.conf.beat_schedule = {
    "weather_info": {
        "task": "weather.tasks.get_weather_info",
        "schedule": crontab(hour=1, minute=00),
        # "schedule": 10,
        "args": {today, today + timedelta(days=6)},
    }
}
