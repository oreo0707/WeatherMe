# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MENU_BGM = os.path.join(BASE_DIR, "assets", "music", "menu_bgm.mp3")

WEATHER_BGM = {
    "sunny":  os.path.join(BASE_DIR, "assets", "music", "sunny_bgm.mp3"),
    "cloudy": os.path.join(BASE_DIR, "assets", "music", "cloudy_bgm.mp3"),
    "rain":   os.path.join(BASE_DIR, "assets", "music", "rain_bgm.mp3"),
    "snow":   os.path.join(BASE_DIR, "assets", "music", "snow_bgm.mp3"),
    "storm":  os.path.join(BASE_DIR, "assets", "music", "storm_bgm.mp3"),
}
