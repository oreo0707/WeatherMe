import requests

API_KEY = "8ff9552d270fa43de7dd61064fc898df"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Weather API error:", e)
        return None

def map_weather(api_weather):
    """
    Maps OpenWeather 'main' field to your asset folder names
    """
    api_weather = api_weather.lower()

    if api_weather in ["clear"]:
        return "sunny"
    if api_weather in ["clouds", "cloudy", "overcast"]:
        return "cloudy"
    if api_weather in ["rain", "drizzle", "showers"]:
        return "rain"
    if api_weather in ["thunderstorm", "storm"]:
        return "storm"
    if api_weather in ["snow", "snowfall"]:
        return "snow"

    return "sunny"  # fallback

def get_city_suggestions(query, limit=5):
    if not query:
        return []

    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": query,
        "limit": limit,
        "appid": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data:
            city = f"{item['name']}, {item['country']}"
            results.append({
                "label": city,
                "lat": item["lat"],
                "lon": item["lon"]
            })

        return results

    except Exception as e:
        print("City autocomplete error:", e)
        return []
