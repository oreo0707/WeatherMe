# main.py
import tkinter as tk
from screens.menu import MenuScreen
from screens.weather import WeatherScreen
from screens.settings import SettingsScreen
from screens.info import InfoScreen
import pygame
from config import MENU_BGM
from utils import resource_path
import threading
import keyboard
import os

WINDOW_WIDTH = 570
WINDOW_HEIGHT = 650

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)

        # Center window
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - WINDOW_WIDTH) // 2
        y = (screen_h - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        self.resizable(False, False)


        # ---------------- State ----------------
        self.current_theme = "light"
        self.current_weather = "sunny"
        self.current_city = None
        self.current_screen = None
        self.current_bgm = None

        # ---------------- Music ----------------
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

        self.current_bgm = None

        # ---------------- Container ----------------
        self.container = tk.Frame(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.container.place(x=0, y=0)

        # ---------------- Screens ----------------
        self.screens = {
            "menu": MenuScreen(self.container, self),
            "weather": WeatherScreen(self.container, self),
            "settings": SettingsScreen(self.container, self),
            "info": InfoScreen(self.container, self)
        }
        for screen in self.screens.values():
            screen.place(x=0, y=0)

        self.show_screen("menu")
        threading.Thread(target=self.register_hotkeys, daemon=True).start()


    # ---------------- Show Screen ----------------
    def show_screen(self, name):
        frame = self.screens[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        if hasattr(frame, "update_theme"):
            frame.update_theme()

    
    def play_menu_music(self):
        if self.current_bgm != "menu":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(resource_path(MENU_BGM))
            pygame.mixer.music.play(-1)
            self.current_bgm = "menu"

    def play_weather_music(self, weather_type):
        bgm_path = f"assets/music/{weather_type}_bgm.mp3"
        if os.path.exists(resource_path(bgm_path)):
            if self.current_bgm != bgm_path:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(resource_path(bgm_path))
                pygame.mixer.music.play(-1)
                self.current_bgm = bgm_path 

    # ---------------- Music ----------------
    def play_bgm(self, screen_name):
        if not path:
            return

        if self.current_bgm == path:
            return 

        pygame.mixer.music.stop()
        pygame.mixer.music.load(resouce_path(path))
        pygame.mixer.music.play(-1)
        self.current_bgm = path

    # ---------------- Click Sound ----------------
    def play_click_sound(self):
        click_path = "assets/music/mouse_click.mp3"
        if os.path.exists(resource_path(click_path)):
            sound = pygame.mixer.Sound(resource_path(click_path))
            sound.play()


    # ---------------- Hide & Restore ----------------
    def hide_window(self):
        self.withdraw() 

    def restore_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    # ---------------- Global Hotkeys ----------------
    def register_hotkeys(self):
        keyboard.add_hotkey("ctrl+r", self.restore_window)
        keyboard.wait()



if __name__ == "__main__":
    app = App()
    app.mainloop()


