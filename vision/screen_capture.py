import pyautogui
import numpy as np
def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    return screenshot