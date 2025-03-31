import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import config

API_KEY = config.OPEN_WEAHTER_API_KEY

def fetch_weather(latitude, longitude, date):
    timestamp = int(date.timestamp())  # 유닉스 타임스탬프 변환
    url = "http://history.openweathermap.org/data/2.5/history/city"

    params = {
        "lat": latitude,
        "lon": longitude,
        "type": "hour",
        "start": timestamp,
        "end": timestamp + 86400,  # 하루 후
        "appid": API_KEY,
        "units": "metric"  # 섭씨 온도
    }

    response = requests.get(url, params=params)
    weather_data = response.json()
    if "list" in weather_data and weather_data["list"]:
        feels_like = [entry["main"]["feels_like"] for entry in weather_data["list"] if "main" in entry and "feels_like" in entry["main"]]
        weather_conditions = [entry["weather"][0]["main"] for entry in weather_data["list"] if "weather" in entry and entry["weather"]]

        if feels_like:
            avg_feels_like = sum(feels_like) / len(feels_like)
        else:
            avg_feels_like = None

        precipitation = 0
        for entry in weather_data["list"]:
            if "rain" in entry and "1h" in entry["rain"]:
                precipitation += entry["rain"]["1h"]

        if weather_conditions:
            most_common_weather = max(set(weather_conditions), key=weather_conditions.count)
        else:
            most_common_weather = "Unknown"

        weather_info = {
            "date": date.strftime('%Y-%m-%d'),
            "feelslike": round(avg_feels_like, 1) if avg_feels_like else None,
            "precipitation": round(precipitation, 1),
            "weather": most_common_weather
        }

        return weather_info
    
    return None