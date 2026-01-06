
# screens/settings.py
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import pygame
import os
from utils import resource_path


WINDOW_WIDTH = 570
WINDOW_HEIGHT = 650
TOP_PANEL_HEIGHT = 86
INNER_WIDTH = 500
INNER_HEIGHT = 500

THEME_ASSETS = {
    "light": {
        "panel_bg": "#fff4f4",
        "content_bg": "white",
        "text": "#ff969d",
        "icons": "assets/screen/settings_light/icons",
        "volume": "assets/volume/volume_bar_light",
        "slider": "assets/theme_toggle/Slide_button.png"
    },
    "dark": {
        "panel_bg": "#26364A",
        "content_bg": "#43597B",
        "text": "#828282",
        "icons": "assets/screen/settings_dark/icons",
        "volume": "assets/volume/volume_bar_dark",
        "slider": "assets/theme_toggle/Dark_button.png"
    }
}


class SettingsScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.app = app
        self.pack_propagate(False)

        self.volume = 5
        self.muted = False

        # ---------------- Fonts ----------------
        self.font_title = tkfont.Font(family="VT323", size=50)
        self.font_large = tkfont.Font(family="VT323", size=35)

        # ---------------- Top Panel ----------------
        self.top_panel = tk.Frame(self, width=WINDOW_WIDTH, height=TOP_PANEL_HEIGHT)
        self.top_panel.place(x=0, y=0)
        self.top_panel.pack_propagate(False)
        self.title_label = tk.Label(self.top_panel, text="Settings", font=self.font_title)
        self.title_label.place(x=20, y=1)

        # Load icons
        self._load_icon_buttons()

        # ---------------- Load Volume Images ----------------
        self._load_volume_images()

        # ---------------- Inner Frame ----------------
        self.inner_frame = tk.Frame(self, width=INNER_WIDTH, height=INNER_HEIGHT)
        self.inner_frame.place(x=(WINDOW_WIDTH - INNER_WIDTH)//2, y=TOP_PANEL_HEIGHT + 20)
        self.inner_frame.pack_propagate(False)

        # ---------------- Build UI ----------------
        self._build_inner_ui()

        # Apply initial theme
        self.update_theme()

    # ---------------- ICON BUTTONS ----------------
    def _load_icon_buttons(self):
        def load_icon(path):
            return ImageTk.PhotoImage(Image.open(resource_path(path)).resize((50, 50)))

        theme = self.app.current_theme
        folder_path = THEME_ASSETS[theme]["icons"]

        self.icons = {
            "back": load_icon(os.path.join(folder_path, f"{theme}_back.png")),
            "minimize": load_icon(os.path.join(folder_path, f"{theme}_minimize.png")),
            "quit": load_icon(os.path.join(folder_path, f"{theme}_quit.png")),
        }

        x = WINDOW_WIDTH - 60
        gap = 60
        tk.Button(self.top_panel, image=self.icons["quit"], bd=0,
                  bg=THEME_ASSETS[theme]["panel_bg"], activebackground=THEME_ASSETS[theme]["panel_bg"],
                  command=lambda: [self.app.play_click_sound(), self.app.quit()]).place(x=x, y=20)
        x -= gap
        tk.Button(self.top_panel, image=self.icons["minimize"], bd=0,
                  bg=THEME_ASSETS[theme]["panel_bg"], activebackground=THEME_ASSETS[theme]["panel_bg"],
                  command=lambda: [self.app.play_click_sound(), self.app.hide_window()]).place(x=x, y=20)
        x -= gap
        tk.Button(self.top_panel, image=self.icons["back"], bd=0,
                  bg=THEME_ASSETS[theme]["panel_bg"], activebackground=THEME_ASSETS[theme]["panel_bg"],
                  command=lambda: [self.app.play_click_sound(), self.open_menu()]).place(x=x, y=20)


    # ---------------- Volume Images ----------------
    def _load_volume_images(self):
        theme = self.app.current_theme
        vol_path = THEME_ASSETS[theme]["volume"]

        self.volume_img = ImageTk.PhotoImage(
            Image.open(
                resource_path(os.path.join(vol_path, "Volume_icon.png"))
            ).resize((70, 70))
        )
        self.mute_img = ImageTk.PhotoImage(
            Image.open(
                resource_path(os.path.join(vol_path, "Mute_icon.png"))
            ).resize((75, 75))
        )
        self.plus_img = ImageTk.PhotoImage(
            Image.open(
                resource_path(os.path.join(vol_path, "VolumeUp_icon.png"))
            ).resize((40, 40))
        )
        self.minus_img = ImageTk.PhotoImage(
            Image.open(
                resource_path(os.path.join(vol_path, "VolumeDown_icon.png"))
            ).resize((40, 40))
        )
        self.volume_bar_imgs = [
            ImageTk.PhotoImage(
                Image.open(
                    resource_path(os.path.join(vol_path, f"Volume_bar{i}.png"))
                ).resize((200, 150))
            ) for i in range(11)
        ]

    # ---------------- UI Elements ----------------
    def _build_inner_ui(self):
        theme = self.app.current_theme
        assets = THEME_ASSETS[theme]

        # Volume Label
        self.volume_label = tk.Label(self.inner_frame, text="Volume:", font=self.font_large)
        self.volume_label.pack(anchor="w", padx=20, pady=(30, 0))

        # Volume Row
        self.vol_row = tk.Frame(self.inner_frame)
        self.vol_row.pack(padx=55, pady=(10, 20))

        self.volume_icon_frame = tk.Frame(self.vol_row, width=75, height=75)
        self.volume_icon_frame.pack(side="left")
        self.volume_icon_frame.pack_propagate(False)

        self.volume_icon_label = tk.Label(
            self.volume_icon_frame, 
            image=self.volume_img, 
            bg=self.inner_frame["bg"]        
        )
        self.volume_icon_label.place(relx=0.5, rely=0.5, anchor="center")
        self.volume_icon_label.bind(
            "<Button-1>",
            lambda e: [
                self.app.play_click_sound(),
                self.toggle_mute()
            ]
        )

        self.minus_btn = tk.Button(self.vol_row, image=self.minus_img, bd=0, command=lambda: self.volume_down())
        self.minus_btn.pack(side="left", padx=5)

        self.volume_canvas = tk.Canvas(self.vol_row, width=200, height=150, bd=0, highlightthickness=0)
        self.volume_canvas.pack(side="left", padx=5)
        self.volume_bar_item = self.volume_canvas.create_image(0, 0, anchor="nw", image=self.volume_bar_imgs[self.volume])

        self.plus_btn = tk.Button(self.vol_row, image=self.plus_img, bd=0, command=lambda: self.volume_up())
        self.plus_btn.pack(side="left", padx=5)

        # Theme Label
        self.theme_label = tk.Label(self.inner_frame, text="Theme:", font=self.font_large)
        self.theme_label.pack(anchor="w", padx=20, pady=(10, 0))

        # Theme Slider Button
        self.slider_light_img = ImageTk.PhotoImage(Image.open(resource_path(THEME_ASSETS["light"]["slider"])).resize((160, 150)))
        self.slider_dark_img = ImageTk.PhotoImage(Image.open(resource_path(THEME_ASSETS["dark"]["slider"])).resize((160, 150)))
        self.slider_btn = tk.Button(self.inner_frame, image=self.slider_light_img, bd=0, highlightthickness=0,
                                    relief="flat", command=self.toggle_theme)
        self.slider_btn.pack(anchor="w", padx=60, pady=(0, 10))

    # ---------------- VOLUME LOGIC ----------------
    def toggle_mute(self, event=None):
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else self.volume / 10)
        self.volume_icon_label.config(image=self.mute_img if self.muted else self.volume_img)
        self.update_volume_bar()

    def volume_up(self):
        if self.muted:
            self.toggle_mute()
        if self.volume < 10:
            self.volume += 1
            pygame.mixer.music.set_volume(self.volume / 10)
            self.update_volume_bar()

    def volume_down(self):
        if self.volume > 0:
            self.volume -= 1
            pygame.mixer.music.set_volume(self.volume / 10)
            self.update_volume_bar()
        if self.volume == 0:
            self.muted = True
            self.volume_icon_label.config(image=self.mute_img)

    def update_volume_bar(self):
        self.volume_canvas.itemconfigure(self.volume_bar_item, image=self.volume_bar_imgs[self.volume])

    # ---------------- THEME LOGIC ----------------
    def toggle_theme(self):
        self.app.current_theme = "dark" if self.app.current_theme == "light" else "light"
        for screen in self.app.screens.values():
            if hasattr(screen, "update_theme"):
                screen.update_theme()

    def update_theme(self):
        theme = self.app.current_theme
        assets = THEME_ASSETS[theme]

        # Top Panel
        self.configure(bg=assets["panel_bg"])
        self.top_panel.configure(bg=assets["panel_bg"])
        self.title_label.config(bg=assets["panel_bg"], fg=assets["text"])
        self._load_icon_buttons()

        # Inner Frame
        self.inner_frame.configure(bg=assets["content_bg"])
        self.volume_icon_frame.configure(bg=assets["content_bg"])
        self.volume_icon_label.config(bg=assets["content_bg"])

        self.vol_row.configure(bg=assets["content_bg"])
        self.volume_canvas.configure(bg=assets["content_bg"])
        self.volume_label.config(bg=assets["content_bg"], fg=assets["text"])
        self.theme_label.config(bg=assets["content_bg"], fg=assets["text"])

        # Reload volume icons & bars
        self._load_volume_images()
        self.volume_icon_label.config(image=self.mute_img if self.muted else self.volume_img)
        self.volume_canvas.itemconfigure(self.volume_bar_item, image=self.volume_bar_imgs[self.volume])
        self.plus_btn.config(image=self.plus_img, bg=assets["content_bg"], activebackground=assets["content_bg"])
        self.minus_btn.config(image=self.minus_img, bg=assets["content_bg"], activebackground=assets["content_bg"])

        # Theme Slider
        self.slider_btn.config(image=self.slider_dark_img if theme=="dark" else self.slider_light_img,
                               bg=assets["content_bg"], activebackground=assets["content_bg"])

    # ---------------- BGM ----------------
    def on_show(self):
        self.app.play_menu_music()  # menu/settings/info screens



    # ---------------- NAVIGATION ----------------
    def open_menu(self):
        self.app.show_screen("menu")

