from utils.url_list import districts_url, open_metro
from utils.helper import get_api_response
from datetime import datetime
import contextlib


def get_districts_weather_data():
    # load districts data
    data = get_api_response(districts_url)
    districts_data = data["districts"]
    print(districts_data)

    for district in districts_data:
        # print(district)
        division = district["division_id"]
        district_name = district["name"]
        district_bn_name = district["bn_name"]
        lat = district["lat"]
        long = district["long"]

        # weather data
        weather_data = get_api_response(
            open_metro.format(
                latitude=lat,
                longitude=long,
                start_date="2023-10-06",
                end_date="2023-10-13",
            )
        )

        # print(weather_data)
        get_2pm_data(weather_data)


def get_2pm_data(data):
    # print(data)
    hourly_data = data["hourly"]
    time = hourly_data["time"]
    temp = hourly_data["temperature_2m"]
    # print(time, temp)

    # split time by date
    date_list = []
    time_list = []

    for i in range(14, len(time), 24):
        # print(time[i], temp[i])
        date, time = date_time_format(time[i])
        date_list.append(date)
        time_list.append(time)
    print(date, time)
    date_time = list(zip(date_list, time_list))
    print(date_time)
    return date_time


def date_time_format(times):
    # format date and time
    date = (datetime.strptime(times, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d"),)
    time = datetime.strptime(times, "%Y-%m-%dT%H:%M").strftime("%H:%M")
    with contextlib.suppress(IndexError):
        date = date[0]
    return date, time
