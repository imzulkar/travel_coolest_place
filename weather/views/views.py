from datetime import datetime, timedelta
import random
from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.models import Weather
from weather.serializers import WeatherSerializer, CoolestWeatherSerializer
from weather.weather import get_districts_weather


def avg_temp(models, limit, date, day_limit):
    """calculate avg temparature for next days"""
    data = models.objects.filter(
        date__gte=date, date__lte=date + timedelta(days=day_limit)
    )  # next 7 days data
    return (
        data.values("district")
        .annotate(avg_value=Avg("temp"))
        .order_by("avg_value")[:limit]
    )


class CoolestDistrictView(APIView):
    """get the coolest district"""

    def get(self, request, format=None):
        # get the coolest district
        today = datetime.now().date()
        data = avg_temp(models=Weather, limit=10, date=today, day_limit=7)
        serializer = CoolestWeatherSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlaceToVisitView(APIView):
    def get(self, request, format=None):
        """
        get the random 1 coolest district to visit
        """
        # get the coolest district
        today = datetime.now().date()
        data = avg_temp(
            models=Weather, limit=10, date=today, day_limit=7
        )  # get specific data from database and limitt data and how many days avg you want
        if data.exists():
            # Select a random object from the queryset
            random_object = random.choice(
                data
            )  # from top 5 coolest district pick one randomly
            serializer = CoolestWeatherSerializer(random_object)
            return Response(serializer.data, status=status.HTTP_200_OK)


class SuggestFriendView(APIView):
    def get_location_info(self, location, date):
        # get location info
        date = datetime.strptime(str(date), "%Y-%m-%d").date()
        return Weather.objects.filter(district__icontains=location, date=date).last()

    def get(self, request, format=None):
        # get value from query lat,lang, date
        location = request.query_params.get("location", None)
        date = request.query_params.get("date", None)
        destination = request.query_params.get("destination", None)
        if location and date and destination:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            destination_weather = self.get_location_info(destination, date)
            current_location_weather = self.get_location_info(location, date)
            # check if data exist
            if destination_weather and current_location_weather:
                serializer = WeatherSerializer(destination_weather)
                current_serializer = WeatherSerializer(current_location_weather)
                # check if destination is cooler than current location
                if destination_weather.temp < current_location_weather.temp:
                    return Response(
                        {
                            "message": "You should go to this place",
                            "destination": serializer.data,
                            "current_location": current_serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "message": "You should not go to this place",
                            "destination": serializer.data,
                            "current_location": current_serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
        return Response({"message": "No Data Found"}, status=status.HTTP_404_NOT_FOUND)
