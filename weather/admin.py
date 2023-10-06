from django.contrib import admin
from weather.models import Weather

# Register your models here.


class WeatherAdmin(admin.ModelAdmin):
    list_display = ("district", "date", "time", "temp")


admin.site.register(Weather, WeatherAdmin)
