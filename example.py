import keyboard
from src.overlay import Overlay

visible = True
current_window = "Steam"  # Имя окна не процесса!
overlay = Overlay(current_window)

def change_visible():
    global visible
    visible = not visible

keyboard.add_hotkey("INSERT", change_visible, timeout=10)


while True:
    overlay.update_overlay(visible)

