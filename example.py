import keyboard
from src.overlay import Overlay

visible = True # imgui menu visible
current_window = "Steam"  # window name
overlay = Overlay(current_window)

def change_visible():
    global visible
    visible = not visible

# external keybind
keyboard.add_hotkey("INSERT", change_visible)

# render overlay
while True:
    overlay.update_overlay(visible)

