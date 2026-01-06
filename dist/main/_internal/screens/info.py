
# screens/info.py
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
from utils import resource_path
import os

WINDOW_WIDTH = 570
WINDOW_HEIGHT = 650
TOP_PANEL_HEIGHT = 86
INNER_WIDTH = 500
INNER_HEIGHT = 525

THEME_ASSETS = {
    "light": {
        "panel_bg": "#fff4f4",
        "content_bg": "white",
        "text": "#ff969d",
        "icons": "assets/screen/settings_light/icons",
        "bg_img": "assets/icons/info_frame.png"
    },
    "dark": {
        "panel_bg": "#26364A",
        "content_bg": "#43597B",
        "text": "#1A1D24",
        "icons": "assets/screen/settings_dark/icons",
        "bg_img": "assets/icons/info_frame_dark.png" 
    }
}

class InfoScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.app = app
        self.pack_propagate(False)

        # ---------------- Fonts ----------------
        self.font_title = tkfont.Font(family="VT323", size=50)
        self.font_large = tkfont.Font(family="VT323", size=35)

        # ---------------- Top Panel ----------------
        self.top_panel = tk.Frame(self, width=WINDOW_WIDTH, height=TOP_PANEL_HEIGHT)
        self.top_panel.place(x=0, y=0)
        self.top_panel.pack_propagate(False)
        self.title_label = tk.Label(self.top_panel, text="Info", font=self.font_title)
        self.title_label.place(x=20, y=1)

        self._load_icon_buttons()

        # ---------------- Inner Frame ----------------
        self.inner_frame = tk.Frame(self, width=INNER_WIDTH, height=INNER_HEIGHT)
        self.inner_frame.place(x=(WINDOW_WIDTH - INNER_WIDTH)//2, y=TOP_PANEL_HEIGHT + 20)
        self.inner_frame.pack_propagate(False)

        # ---------------- Background ----------------
        self.bg_img = None
        self.bg_label = tk.Label(self.inner_frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Apply initial theme
        self.update_theme()

    # ---------------- Top Panel Icons ----------------
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

    # ---------------- THEME LOGIC ----------------
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
 

        # Background image
        bg_img_path = assets["bg_img"]
        self.bg_img = ImageTk.PhotoImage(Image.open(resource_path(bg_img_path)).resize((INNER_WIDTH, INNER_HEIGHT)))
        self.bg_label.config(image=self.bg_img)

    # ---------------- Show Screen Event ----------------
    def on_show(self):
        self.app.play_menu_music()



    # ---------------- NAVIGATION ----------------
    def open_menu(self):
        self.app.show_screen("menu")
    
