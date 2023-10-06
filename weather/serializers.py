from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from weather.models import Weather


class WeatherSerializer(ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class CoolestWeatherSerializer(ModelSerializer):
    avg_value = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Weather
        fields = [
            "district",
            "avg_value",
        ]
