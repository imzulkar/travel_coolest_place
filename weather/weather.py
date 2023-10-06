import requests
from utils.url_list import districts_url


def get_districts_data():
    response = requests.get(districts_url)
    print(response.json())
    return response.json()
