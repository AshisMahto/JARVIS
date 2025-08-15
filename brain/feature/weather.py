import requests

API_KEY = "YOUR_OPEN_WETHER_API_KEYS"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return None, data.get("message", "Error getting weather data")

        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (f"The weather in {city_name} is currently {weather_desc} "
                          f"with a temperature of {temp}°C, feels like {feels_like}°C. "
                          f"Humidity is {humidity} percent, and wind speed is {wind_speed} meters per second.")

        return weather_report, None

    except Exception as e:
        return None, str(e)
