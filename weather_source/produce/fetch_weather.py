# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("OPENWEATHER_API_KEY")
# LAT_JKT = os.getenv("LATITUDE", "-6.2146")
# LON_JKT = os.getenv("LONGITUDE", "106.8451")

# LAT_SBY = os.getenv("LATITUDE", "-7.2575")
# LON_SBY = os.getenv("LONGITUDE", "112.7521")


# def fetch_weather_data():
#     url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT_JKT}&lon={LON_JKT}&appid={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error fetching data: {response.status_code}")
#         return None


import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

LAT_JKT = os.getenv("LATITUDE_JKT", "-6.2146")
LON_JKT = os.getenv("LONGITUDE_JKT", "106.8451")

LAT_SBY = os.getenv("LATITUDE_SBY", "-7.2575")
LON_SBY = os.getenv("LONGITUDE_SBY", "112.7521")

def fetch_weather_data(lat: str, lon: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def fetch_weather_data_jkt():
    return fetch_weather_data(LAT_JKT, LON_JKT)

def fetch_weather_data_sby():
    return fetch_weather_data(LAT_SBY, LON_SBY)