from vision.screen_capture import capture_screen
from vision.ocr_reader import OCRReader
from vision.text_locator import find_text
from automation.mouse_controller import move_and_click, start_scroll, stop_scroll
import numpy as np


class ActionPlanner:

    def __init__(self):
        self.ocr = OCRReader()

    def execute(self, command):

        if not command:
            return

        intent = command.get("intent")
        entity = command.get("entities", {}).get("object")
        direction = command.get("entities", {}).get("direction")
        text = command.get("text", "").lower()

        # -------------------------
        # FALLBACK DIRECTION DETECTION
        # -------------------------
        if intent == "scroll" and not direction:

            if "up" in text:
                direction = "up"

            elif "down" in text:
                direction = "down"

        # -------------------------
        # CLICK ACTION
        # -------------------------
        if intent == "click" and entity:

            img = capture_screen()
            img = np.array(img)

            detections = self.ocr.read_text(img)

            pos = find_text(detections, entity)

            if pos:
                x, y = pos
                move_and_click(x, y)
                print(f"Clicked '{entity}' at {pos}")
            else:
                print(f"Could not find '{entity}' on screen")

        # -------------------------
        # SCROLL ACTION
        # -------------------------
        elif intent == "scroll":

            if direction == "up":
                start_scroll("up")
                print("Scrolling up...")

            elif direction == "down":
                start_scroll("down")
                print("Scrolling down...")

            # scroll to object
            elif entity:

                img = capture_screen()
                img = np.array(img)

                detections = self.ocr.read_text(img)

                pos = find_text(detections, entity)

                if pos:
                    x, y = pos

                    move_and_click(x, y)

                    start_scroll("down")  # continuous scroll
                    print(f"Scrolling near '{entity}'")

                else:
                    print(f"Could not find '{entity}' to scroll")

        # -------------------------
        # STOP ACTION
        # -------------------------
        elif intent == "stop":

            stop_scroll()
            print("Scrolling stopped")