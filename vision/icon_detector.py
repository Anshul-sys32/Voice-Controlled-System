import pyautogui


def find_icon(icon_path):

    location = pyautogui.locateOnScreen(icon_path, confidence=0.6, grayscale=True)

    if location:
        return pyautogui.center(location)

    return None