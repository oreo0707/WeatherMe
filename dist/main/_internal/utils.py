import os
import sys
from PIL import Image, ImageTk

def load_screen_background(screen_name, theme):
    """
    screen_name: 'menu', 'info', 'settings', or weather type like 'sunny'
    theme: 'light' or 'dark'
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(BASE_DIR)

    folder_path = os.path.join(
        ROOT_DIR, "assets", "screen", f"{screen_name}_{theme}", "backgrounds"
    )

    if not os.path.exists(folder_path):
        print(f"Background folder not found: {folder_path}")
        return None

    bg_files = sorted(
        f for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    )

    if not bg_files:
        print(f"No background image found in {folder_path}")
        return None

    bg_path = resource_path(os.path.join(folder_path, bg_files[0]))

    try:
        image = Image.open(bg_path).resize((570, 650))
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"[Theme] Failed to load background {bg_path}: {e}")
        return None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)