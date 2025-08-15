# radar.py

import requests

def get_radar_image(city, speak):
    api_key = "YOUR_OPENWEATHER_API_KEY"
    
    # Get coordinates for city
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_res = requests.get(geo_url).json()
    
    if not geo_res:
        speak("I couldn't find that location.")
        return
    
    lat = geo_res[0]["lat"]
    lon = geo_res[0]["lon"]

    # Prepare radar tile image URL
    tile_url = f"https://tile.openweathermap.org/map/precipitation_new/10/{int(lon)}/{int(lat)}.png?appid={api_key}"

    speak(f"Here is the radar image for {city}.")
    print(f"🛰️ Radar image URL: {tile_url}")
