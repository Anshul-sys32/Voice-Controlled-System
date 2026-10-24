import pyautogui
import random
import time
import threading

# GLOBAL STATE
scrolling = False
scroll_thread = None


def move_and_click(x, y):

    pyautogui.moveTo(
        x,
        y,
        duration=random.uniform(0.3, 0.8)
    )

    pyautogui.click()


def _scroll_worker(direction, speed=5, delay=0.05):
    global scrolling

    while scrolling:

        if direction == "up":
            pyautogui.scroll(speed)

        elif direction == "down":
            pyautogui.scroll(-speed)

        time.sleep(delay)


def start_scroll(direction):
    global scrolling, scroll_thread

    if scrolling:
        return

    scrolling = True

    scroll_thread = threading.Thread(
        target=_scroll_worker,
        args=(direction,),
        daemon=True
    )

    scroll_thread.start()


def stop_scroll():
    global scrolling
    scrolling = False

def move_relative(distance, direction):
    import pyautogui
    import random

    x, y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()

    dx, dy = 0, 0
    direction = direction.lower().strip()

    if direction in ["up", "top"]:
        dy = -distance
    elif direction in ["down", "bottom"]:
        dy = distance
    elif direction == "left":
        dx = -distance
    elif direction == "right":
        dx = distance
    elif direction in ["top-right"]:
        dx = distance
        dy = -distance
    elif direction in ["top-left"]:
        dx = -distance
        dy = -distance
    elif direction in ["bottom-right"]:
        dx = distance
        dy = distance
    elif direction in ["bottom-left"]:
        dx = -distance
        dy = distance

    # 🔥 Clamp inside screen bounds (IMPORTANT)
    new_x = max(10, min(screen_width - 10, x + dx))
    new_y = max(10, min(screen_height - 10, y + dy))

    pyautogui.moveTo(
        new_x,
        new_y,
        duration=random.uniform(0.2, 0.5)
    )

def perform_click(click_type="left"):
    """
    Perform different types of clicks at current mouse position
    """

    if click_type == "left":
        pyautogui.click()

    elif click_type == "right":
        pyautogui.click(button="right")

    elif click_type == "double":
        pyautogui.doubleClick()

    elif click_type == "middle":
        pyautogui.click(button="middle")