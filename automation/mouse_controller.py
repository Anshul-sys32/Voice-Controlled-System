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