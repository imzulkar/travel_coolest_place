import contextlib
from utils.helper import get_api_response
from utils.url_list import open_metro, districts_url
from datetime import datetime, timedelta
from weather.models import Weather


def get_coordinates(district):
    # destructure the district data
    latitude = district["lat"]
    longitude = district["long"]
    district_name = district["name"]
    return latitude, longitude, district_name


def get_forcast_time_and_temperature(forcast_data):
    # destructure time and temperature from api response
    times = forcast_data["hourly"]["time"]
    temperatures = forcast_data["hourly"]["temperature_2m"]
    return times, temperatures


def weather_informations(latitude, longitude, start_date, end_date):
    # weather informations fetch from open-metro api
    print(f"weather_informations- {start_date}{end_date}")
    url = open_metro.format(
        latitude=latitude, longitude=longitude, start_date=start_date, end_date=end_date
    )
    return get_api_response(url)


def date_time_format(times):
    # format date and time
    date = (datetime.strptime(times, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d"),)
    time = datetime.strptime(times, "%Y-%m-%dT%H:%M").strftime("%H:%M")
    with contextlib.suppress(IndexError):
        date = date[0]
    return date, time


def store_2pm_temperature(district_name, times, temperatures):
    # store every day 2pm/14  temperature in database
    for i in range(12, len(times), 24):
        date, time = date_time_format(times[i + 2])
        print(district_name, date, time, temperatures[i])
        weather, created = Weather.objects.get_or_create(
            district=district_name, date=date, time=time, temp=temperatures[i]
        )
    return district_name


def get_districts_weather(start_date=None, end_date=None):
    # this function will execute every day using periodic task

    districts = get_api_response(districts_url)  # fetch districts data from github
    for district in districts["districts"]:
        latitude, longitude, district_name = get_coordinates(district)

        # Fetch temperature data for the next 7 days at 2 PM
        forcast_data = weather_informations(
            latitude, longitude, start_date, end_date
        )  # fetch data from open-metro api
        times, temperatures = get_forcast_time_and_temperature(
            forcast_data
        )  # get time and temperature from api response
        store_2pm_temperature(
            district_name, times, temperatures
        )  # store 2pm temperature in database

    return True
