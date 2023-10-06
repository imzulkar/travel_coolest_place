from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import datetime, timedelta
from weather.weather import get_districts_weather

app = Celery()


# @app.task
# def test():
#     print("runnning test task")


@app.task
def get_weather_info(start_date=None, end_date=None):
    if start_date is None:
        today = datetime.now().date()
        start_date = today
        end_date = today + timedelta(days=7)
    print(start_date, end_date)
    get_districts_weather(start_date, end_date)
