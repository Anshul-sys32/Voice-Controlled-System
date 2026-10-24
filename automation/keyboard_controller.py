import pyautogui
import time
import random


def type_text(text, delay=0.05):
    """
    Types text like a human (slight randomness)
    """
    for char in text:
        pyautogui.write(char)
        time.sleep(delay + random.uniform(0.01, 0.05))


def press_key(key):
    """
    Press a single key (enter, esc, tab, etc.)
    """
    pyautogui.press(key)


def hotkey(*keys):
    """
    Example: ctrl+c, ctrl+v, alt+tab
    """
    pyautogui.hotkey(*keys)