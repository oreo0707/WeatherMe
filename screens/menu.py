# screens/menu.py
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import os
from services.weather_api import get_city_suggestions
from config import MENU_BGM
from utils import resource_path


WINDOW_WIDTH = 570
WINDOW_HEIGHT = 650
TOP_PANEL_HEIGHT = 86
INNER_WIDTH = 500
INNER_HEIGHT = 525

THEME_ASSETS = {
    "light": {
        "panel_bg": "#fff4f4",
        "content_bg": "white",
        "text": "#f5a7ad",
        "icons": "assets/screen/menu_light/icons",
        "background": "assets/screen/menu_light/backgrounds/menu_light_background.PNG",
        "entry_bg": "assets/icons/enter_bar.png",
        "submit": "assets/icons/submit_button.png",
        "submit_clicked": "assets/icons/submit_button_clicked.png",
        "listbox_bg": "white",
        "listbox_fg": "#f5a7ad",
        "listbox_select_bg": "white",
        "listbox_select_fg": "#f5a7ad",
        "entry_bg_color": "white",
        "entry_fg_color": "#f5a7ad",
        "entry_cursor": "#f5a7ad",
    },
    "dark": {
        "panel_bg": "#000000",
        "content_bg": "#43597B",
        "text": "#3066A8",
        "icons": "assets/screen/menu_dark/icons",
        "background": "assets/screen/menu_dark/backgrounds/menu_dark_background.PNG",
        "entry_bg": "assets/icons/enter_bar_dark.png",
        "submit": "assets/icons/submit_button_dark.png",
        "submit_clicked": "assets/icons/submit_button_dark_clicked.png",
        "listbox_bg": "#1a2d3c",
        "listbox_fg": "#4F80C1",
        "listbox_select_bg": "#1a2d3c",
        "listbox_select_fg": "#4F80C1",
        "entry_bg_color": "#1a2d3c",
        "entry_fg_color": "#4f80c1",
        "entry_cursor": "#4f80c1"
    }
}


class MenuScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.app = app
        self.pack_propagate(False)

        # ---------------- Fonts ----------------
        self.font_title = tkfont.Font(family="VT323", size=50)
        self.font_large = tkfont.Font(family="VT323", size=35)
        self.font_medium = tkfont.Font(family="VT323", size=18)

        # ---------------- Top Panel ----------------
        self.top_panel = tk.Frame(self, width=WINDOW_WIDTH, height=TOP_PANEL_HEIGHT)
        self.top_panel.place(x=0, y=0)
        self.top_panel.pack_propagate(False)
        self.header_label = tk.Label(self.top_panel, text="Weather Me", font=self.font_title)
        self.header_label.place(x=20, y=1)

        self._load_icon_buttons()

        # ---------------- Inner Canvas ----------------
        self.inner_canvas = tk.Canvas(
            self,
            width=INNER_WIDTH,
            height=INNER_HEIGHT,
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.inner_canvas.place(x=(WINDOW_WIDTH - INNER_WIDTH)//2, y=TOP_PANEL_HEIGHT)

        # Load theme and build UI
        self.city_var = tk.StringVar()
        self._build_ui()
        self.update_theme()

    # ---------------- Top Panel Icons ----------------
    def _load_icon_buttons(self):
        def load_icon(path):
            return ImageTk.PhotoImage(Image.open(resource_path(path)).resize((50, 50)))

        theme = self.app.current_theme
        folder_path = THEME_ASSETS[theme]["icons"]
        assets = THEME_ASSETS[theme]

        # Load images
        self.icons = {
            "settings": load_icon(os.path.join(folder_path, f"{theme}_settings.png")),
            "info": load_icon(os.path.join(folder_path, f"{theme}_info.png")),
            "minimize": load_icon(os.path.join(folder_path, f"{theme}_minimize.png")),
            "quit": load_icon(os.path.join(folder_path, f"{theme}_quit.png")),
        }

        x = WINDOW_WIDTH - 60
        gap = 60

        # Quit label
        self.quit_label = tk.Label(self.top_panel, image=self.icons["quit"], bg=assets["panel_bg"])
        self.quit_label.place(x=x, y=20)
        self.quit_label.bind("<Button-1>", lambda e: [self.app.play_click_sound(), self.app.quit()])

        x -= gap
        # Minimize label
        self.min_label = tk.Label(self.top_panel, image=self.icons["minimize"], bg=assets["panel_bg"])
        self.min_label.place(x=x, y=20)
        self.min_label.bind("<Button-1>", lambda e: [self.app.play_click_sound(), self.app.hide_window()])

        x -= gap
        # Info label
        self.info_label = tk.Label(self.top_panel, image=self.icons["info"], bg=assets["panel_bg"])
        self.info_label.place(x=x, y=20)
        self.info_label.bind("<Button-1>", lambda e: [self.app.play_click_sound(), self.open_info()])

        x -= gap
        # Settings label
        self.settings_label = tk.Label(self.top_panel, image=self.icons["settings"], bg=assets["panel_bg"])
        self.settings_label.place(x=x, y=20)
        self.settings_label.bind("<Button-1>", lambda e: [self.app.play_click_sound(), self.open_settings()])

    # ---------------- Build UI on Canvas ----------------
    def _build_ui(self):
        theme = self.app.current_theme
        assets = THEME_ASSETS[theme]

        # Background image
        bg_img = Image.open(resource_path(assets["background"])).resize((INNER_WIDTH, INNER_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        self.inner_canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        self.bg_item = self.inner_canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)


        # Label text
        self.label_text_item = self.inner_canvas.create_text(
            INNER_WIDTH//2, 100,
            text="Enter your city:",
            font=self.font_large,
            fill=assets["text"]
        )
        # Entry background image
        entry_bg_img = Image.open(resource_path(assets["entry_bg"])).resize((380, 50))
        self.entry_bg_photo = ImageTk.PhotoImage(entry_bg_img)
        self.inner_canvas.create_image(75, 110, anchor="nw", image=self.entry_bg_photo)
        self.entry_bg_item = self.inner_canvas.create_image(70, 160, anchor="nw", image=self.entry_bg_photo)

        # Entry widget as window on canvas
        self.city_entry = tk.Entry(
            self.inner_canvas,
            textvariable=self.city_var,
            font=self.font_medium,
            bd=0,
            highlightthickness=0,
            relief="flat",
            bg=assets["entry_bg_color"],
            fg=assets["entry_fg_color"],
            insertbackground=assets["entry_cursor"]
        )
        self.inner_canvas.create_window(93, 170, anchor="nw", width=320, height=32, window=self.city_entry)


        # Listbox for suggestions
        self.city_listbox = tk.Listbox(
            self.inner_canvas,
            font=self.font_medium,
            height=5,
            bd=0,
            highlightthickness=0
        )
        # Place it on canvas slightly below the entry
        self.city_listbox_window = self.inner_canvas.create_window(
            90, 210,
            anchor="nw",
            width=320,
            window=self.city_listbox
        )

        # Hide initially
        self.inner_canvas.itemconfigure(self.city_listbox_window, state='hidden')


        # Bind events
        self.city_entry.bind("<KeyRelease>", self.on_city_typing)
        self.city_listbox.bind("<<ListboxSelect>>", self.on_city_select)

        # For debounce
        self.city_typing_job = None
        self.city_results = []


        # Submit button as canvas image
        submit_img = Image.open(resource_path(assets["submit"])).resize((240, 100))
        submit_clicked_img = Image.open(resource_path(assets["submit_clicked"])).resize((240, 100))
        self.submit_photo = ImageTk.PhotoImage(submit_img)
        self.submit_clicked_photo = ImageTk.PhotoImage(submit_clicked_img)
        self.submit_item = self.inner_canvas.create_image(130, 300, anchor="nw", image=self.submit_photo)
        self.inner_canvas.tag_bind(self.submit_item, "<Button-1>", self._on_submit_click)

    def _on_submit_click(self, event):
        self.inner_canvas.itemconfigure(self.submit_item, image=self.submit_clicked_photo)
        self.after(100, lambda: [self.app.play_click_sound(), self.inner_canvas.itemconfigure(self.submit_item, image=self.submit_photo)])
        self.submit_city()

    # ---------------- Navigation ----------------
    def open_settings(self):
        self.app.show_screen("settings")

    def open_info(self):
        self.app.show_screen("info")

    def submit_city(self):
        city = self.city_var.get().strip()
        if city:
            self.app.current_city = city
            self.app.show_screen("weather")

    # ---------------- Theme Update ----------------
    def update_theme(self):
        theme = self.app.current_theme
        assets = THEME_ASSETS[theme]

        # Top panel colors
        self.configure(bg=assets["panel_bg"])
        self.top_panel.config(bg=assets["panel_bg"])
        self.header_label.config(bg=assets["panel_bg"], fg=assets["text"])

        # Update existing background image instead of creating a new one
        bg_img = Image.open(resource_path(assets["background"])).resize((INNER_WIDTH, INNER_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        self.inner_canvas.itemconfig(self.bg_item, image=self.bg_photo)

        # Update text color
        self.inner_canvas.itemconfig(self.label_text_item, fill=assets["text"])

        # Update entry background image
        entry_bg_img = Image.open(resource_path(assets["entry_bg"])).resize((380, 50))
        self.entry_bg_photo = ImageTk.PhotoImage(entry_bg_img)
        self.inner_canvas.itemconfig(self.entry_bg_item, image=self.entry_bg_photo) 

        # Update entry fg
        self.city_entry.config(
            bg=assets["entry_bg_color"],
            fg=assets["entry_fg_color"],
            insertbackground=assets["entry_cursor"],
            highlightbackground=assets["entry_bg_color"],
            highlightcolor=assets["entry_bg_color"]
        )

        self.inner_canvas.itemconfigure(self.city_listbox_window, state='hidden')

        # Update icons
        self._load_icon_buttons()


        # Update submit button image
        submit_img = Image.open(resource_path(assets["submit"])).resize((240, 100))
        submit_clicked_img = Image.open(resource_path(assets["submit_clicked"])).resize((240, 100))
        self.submit_photo = ImageTk.PhotoImage(submit_img)
        self.submit_clicked_photo = ImageTk.PhotoImage(submit_clicked_img)
        self.inner_canvas.itemconfig(self.submit_item, image=self.submit_photo)

        # Update listbox
        self.city_listbox.config(
            bg=assets["listbox_bg"],
            fg=assets["listbox_fg"],
            selectbackground=assets["listbox_select_bg"],
            selectforeground=assets["listbox_select_fg"],
            activestyle="none",
            cursor="hand2"
        )


    def on_city_typing(self, event):
        if self.city_typing_job:
            self.after_cancel(self.city_typing_job)
        self.city_typing_job = self.after(400, self.fetch_city_suggestions)

    def on_city_select(self, event):
        if not self.city_listbox.curselection():
            return

        index = self.city_listbox.curselection()[0]
        selected = self.city_results[index]

        self.city_var.set(selected["label"])
        self.inner_canvas.itemconfigure(self.city_listbox_window, state='hidden')

        # Save precise location
        self.app.current_city = selected["label"]
        self.app.current_lat = selected["lat"]
        self.app.current_lon = selected["lon"]
        
    def fetch_city_suggestions(self):
        query = self.city_var.get().strip()
        if len(query) < 2:
            self.inner_canvas.itemconfigure(self.city_listbox_window, state='hidden')
            return

        results = get_city_suggestions(query)
        self.city_results = results

        if not results:
            self.inner_canvas.itemconfigure(self.city_listbox_window, state='hidden')
            return

        self.city_listbox.delete(0, tk.END)
        for r in results:
            self.city_listbox.insert(tk.END, r["label"])

        self.inner_canvas.itemconfigure(self.city_listbox_window, state='normal')

    def on_show(self):
        self.app.play_menu_music()

