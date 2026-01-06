# screens/weather.py
import os
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime
from services.weather_api import get_current_weather, map_weather
from config import WEATHER_BGM, MENU_BGM
import pygame
from utils import resource_path


WINDOW_WIDTH = 570
WINDOW_HEIGHT = 650

# Define colors for each weather type
WEATHER_INFO_COLORS = {
    "sunny": {
        "light":{
            "header": "#ffd695",
            "temp": "#fffb93",
            "desc_time": "#fffb93",
            "stats": "#ff9500"
        },
        "dark": {
            "header": "#D38200",
            "temp": "#A77023",
            "desc_time": "#A77023",
            "stats": "#CEB655"
        }
    },
    "cloudy": {
        "light":{
            "header": "#a2c0b7",
            "temp": "#B8E0D4",
            "desc_time": "#B8E0D4",
            "stats": "#344E41"
        },
        "dark": {
            "header": "#567269",
            "temp": "#56746A",
            "desc_time": "#56746A",
            "stats": "#799F93"
        }
    },

    "rain": {
        "light":{
            "header": "#76b0d6",
            "temp": "#A2D7F9",
            "desc_time": "#A2D7F9",
            "stats": "#CCEBFF"
        },
        "dark": {
            "header": "#517B95",
            "temp": "#456B83",
            "desc_time": "#456B83",
            "stats": "#457286"
        }
    },
    "snow": {
        "light":{
            "header": "#29FBFF",
            "temp": "#8EFDFF",
            "desc_time": "#8EFDFF",
            "stats": "#43D9F0"
        },
        "dark": {
            "header": "#263348",
            "temp": "#2D4052",
            "desc_time": "#2D4052",
            "stats": "#192935"
        }
    },
    "storm": {
        "light":{
            "header": "#011127",
            "temp": "#767676",
            "desc_time": "#767676",
            "stats": "#6B8299"
        },
        "dark": {
            "header": "000000",
            "temp": "#505050",
            "desc_time": "#505050",
            "stats": "#6B6B6B"
        }
    }
}

HEADER_COLORS = {
    "sunny":  "#ffd695",
    "cloudy": "#a2c0b7",
    "rain":   "#76b0d6",
    "snow":   "#b8fbff",
    "storm":  "#011127"
}

class WeatherScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.app = app
        self.pack_propagate(False)

        # ---------------- Fonts ----------------
        self.font_title = tkfont.Font(family="VT323", size=48)
        self.font_temp = tkfont.Font(family="VT323", size=85)
        self.font_date = tkfont.Font(family="VT323", size=16)
        self.font_text = tkfont.Font(family="VT323", size=22)


        # ---------------- Canvas ----------------
        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0)
        self.bg_photo = None

        # Header and weather text
        self.header_text_id = self.canvas.create_text(20, 5, anchor="nw", text="Weather", font=self.font_title, fill="#ffffff")
        self.temp_text_id = self.canvas.create_text(30, 70, anchor="nw", text="--°C", font=self.font_temp, fill="#b8e0d4")
        self.desc_text_id = self.canvas.create_text(300, 185, anchor="nw", text="--", font=self.font_date, fill="white")
        self.time_text_id = self.canvas.create_text(300, 120, anchor="nw", text="--", font=self.font_date, fill="white")
        self.stat_ids = {}

        start_x = 30
        start_y = 250
        gap = 45  # ← controls vertical spacing (increase for wider gaps)

        self.stat_ids["location"] = self.canvas.create_text(
            start_x, start_y,
            anchor="nw", text="Location: --",
            font=self.font_text, fill="#ffffff"
        )

        self.stat_ids["precipitation"] = self.canvas.create_text(
            start_x, start_y + gap,
            anchor="nw", text="Precipitation: --",
            font=self.font_text, fill="#ffffff"
        )

        self.stat_ids["humidity"] = self.canvas.create_text(
            start_x, start_y + gap * 2,
            anchor="nw", text="Humidity: --%",
            font=self.font_text, fill="#ffffff"
        )

        self.stat_ids["wind"] = self.canvas.create_text(
            start_x, start_y + gap * 3,
            anchor="nw", text="Wind: -- km/h",
            font=self.font_text, fill="#ffffff"
        )



        # Icon images
        self.icons = {}
        self.icon_ids = {}

        # ---------------- Load default theme ----------------
        self.app.current_weather = "sunny"
        self.app.current_theme = "light"
        self.load_weather_theme()

        # ---------------- Weather Animation ----------------
        self.weather_frames = {}   # cache {(weather, theme): frames}
        self.frames = []
        self.frame_index = 0
        self.animating = False


        

    # ---------------- Load background and icons ----------------
    def load_weather_theme(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        weather = self.app.current_weather
        theme = self.app.current_theme
        colors = WEATHER_INFO_COLORS[weather][theme]
        base = os.path.join(BASE_DIR, "assets", "screen", f"{weather}_{theme}")

        # Background
        bg_path = os.path.join(base, "backgrounds", f"{weather}_1.png")
        print("Loading background from:", bg_path)
        full_path = resource_path(bg_path)
        # Draw background first
        if os.path.exists(full_path):
            img = Image.open(full_path).resize((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.bg_photo = ImageTk.PhotoImage(img)
            if hasattr(self, "bg_item"):
                self.canvas.itemconfig(self.bg_item, image=self.bg_photo)
            else:
                self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
            
            self.canvas.tag_lower(self.bg_item)

        else:
            print("Missing background:", bg_path)

        # Icons
        def load_icon(name):
            path = os.path.join(base, "icons", f"{weather}_{name}.png")
            full_path = resource_path(path)
            if os.path.exists(full_path):
                return ImageTk.PhotoImage(Image.open(full_path).resize((50, 50)))
            print("Missing icon:", path)
            return None

        self.icons["back"] = load_icon("back")
        self.icons["minimize"] = load_icon("minimize")
        self.icons["quit"] = load_icon("quit")

        # Draw icons as canvas images for transparency
        for key in ["back", "minimize", "quit"]:
            if key in self.icon_ids:
                self.canvas.delete(self.icon_ids[key])

        if self.icons["back"]:
            self.icon_ids["back"] = self.canvas.create_image(WINDOW_WIDTH - 180, 20, anchor="nw", image=self.icons["back"])
            self.canvas.tag_bind(self.icon_ids["back"], "<Button-1>", lambda e: [self.app.play_click_sound(), self.open_menu()])
        if self.icons["minimize"]:
            self.icon_ids["minimize"] = self.canvas.create_image(WINDOW_WIDTH - 120, 20, anchor="nw", image=self.icons["minimize"])
            self.canvas.tag_bind(self.icon_ids["minimize"], "<Button-1>", lambda e: [self.app.play_click_sound(), self.app.withdraw()])
        if self.icons["quit"]:
            self.icon_ids["quit"] = self.canvas.create_image(WINDOW_WIDTH - 60, 20, anchor="nw", image=self.icons["quit"])
            self.canvas.tag_bind(self.icon_ids["quit"], "<Button-1>", lambda e: [self.app.play_click_sound(), self.app.quit()])

        
        # Update text colors dynamically
        self.canvas.itemconfig(self.header_text_id, fill=colors["header"])
        self.canvas.itemconfig(self.temp_text_id, fill=colors["temp"])
        self.canvas.itemconfig(self.time_text_id, fill=colors["desc_time"])
        self.canvas.itemconfig(self.desc_text_id, fill=colors["desc_time"])
        for stat_id in self.stat_ids.values():
            self.canvas.itemconfig(stat_id, fill=colors["stats"])

        # Header color
        self.canvas.itemconfig(self.header_text_id, text=weather.title(), fill=HEADER_COLORS.get(weather, "#ffffff"))

    # ---------------- Update time ----------------
    def on_show(self):
        self.update_time()
        self.fetch_weather()

    def update_time(self):
        now = datetime.now()
        self.canvas.itemconfig(self.time_text_id, text=now.strftime("%A, %d %B %Y\n%H:%M:%S"))
        self.after(1000, self.update_time)

    # ---------------- Fetch weather ----------------
    def fetch_weather(self):
        try:
            city = self.app.current_city
            if not city:
                return
            data = get_current_weather(city)
            if not data:
                print("Weather not found, staying on menu.")
                self.app.show_screen("menu")
                return

            api_weather = data["weather"][0]["main"]
            self.app.current_weather = map_weather(api_weather)
            self.load_weather_theme() 
            self.start_weather_animation(self.app.current_weather)


            temp = round(data["main"]["temp"])
            desc = data["weather"][0]["description"].title()
            location = data["name"]

            precipitation = 0.0

            if "rain" in data:
                precipitation = data["rain"].get("1h", data["rain"].get("3h", 0.0))
            elif "snow" in data:
                precipitation = data["snow"].get("1h", data["snow"].get("3h", 0.0))

            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            

            # Update canvas labels
            self.canvas.itemconfig(self.temp_text_id, text=f"{temp}°C")
            self.canvas.itemconfig(self.desc_text_id, text=desc)
            stats_text = f"Location: {location}\nPrecipitation: {precipitation} mm\nHumidity: {humidity}%\nWind: {wind} km/h"
            self.canvas.itemconfig(self.stat_ids["location"], text=f"Location: {location}")
            self.canvas.itemconfig(
                self.stat_ids["precipitation"],
                text=f"Precipitation: {precipitation} mm"
            )
            self.canvas.itemconfig(
                self.stat_ids["humidity"],
                text=f"Humidity: {humidity}%"
            )
            self.canvas.itemconfig(
                self.stat_ids["wind"],
                text=f"Wind: {wind} km/h"
            )

            self.app.play_weather_music(self.app.current_weather)



        except Exception as e:
            print("Weather API error:", e)
            self.app.show_screen("menu")

    def play_weather_music(self, weather):
        path = WEATHER_BGM.get(weather)
        if path and os.path.exists(resource_path(path)):
            self.app.play_bgm(resource_path(path))


    def update_theme(self):
        theme = self.app.current_theme

        # Background
        bg_path = f"assets/screen/sunny_{theme}/backgrounds/weather_bg.png"
        full_path = resource_path(bg_path)
        if os.path.exists(full_path):
            bg_img = Image.open(full_path).resize((570, 650))
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        # Icons (like weather icon)
        weather_icon = f"{self.app.current_weather}_{theme}.png"
        icon_path = f"assets/screen/sunny_{theme}/icons/{weather_icon}"
        full_path = resource_path(icon_path)
        if os.path.exists(full_path):
            img = Image.open(full_path).resize((150, 150))
            self.weather_photo = ImageTk.PhotoImage(img)
            self.canvas.itemconfigure(self.weather_icon_id, image=self.weather_photo)

    # ---------------- Navigation ----------------
    def open_menu(self):
        self.app.show_screen("menu")

    def start_weather_animation(self, weather):
        theme = self.app.current_theme
        key = (weather, theme)

        self.frame_index = 0
        self.animating = True

        if key not in self.weather_frames or not self.weather_frames[key]:
            self.weather_frames[key] = load_weather_frames(
                weather,
                theme,
                (WINDOW_WIDTH, WINDOW_HEIGHT)
            )

        self.frames = self.weather_frames[key]
        self.animate_weather()

    def animate_weather(self):
        if not self.animating or not self.frames:
            return

        frame = self.frames[self.frame_index]
        self.canvas.itemconfig(self.bg_item, image=frame)

        self.frame_index = (self.frame_index + 1) % len(self.frames)

        # Adjust delay so full animation loop lasts ~1.6 seconds for all weather types
        total_duration = 1600 
        frame_count = len(self.frames)
        delay = max(total_duration // frame_count, 50) 
        self.after(delay, self.animate_weather)



def load_weather_frames(weather, theme, size):
    folder = resource_path(os.path.join("assets", "screen", f"{weather}_{theme}", "backgrounds"))
    frames = []

    if not os.path.exists(resource_path(folder)):
        print("Weather folder not found:", folder)
        return frames

    for file in sorted(os.listdir(folder)):
        if file.lower().endswith((".png", ".jpg", ".webp")):
            img = Image.open(resource_path(os.path.join(folder, file))).resize(size)
            frames.append(ImageTk.PhotoImage(img))

    print(f"Loaded {len(frames)} frames for {weather} ({theme})")
    return frames


