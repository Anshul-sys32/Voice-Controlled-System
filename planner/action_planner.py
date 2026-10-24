from vision.screen_capture import capture_screen
from vision.ocr_reader import OCRReader
from vision.text_locator import find_text
from automation.mouse_controller import move_and_click, start_scroll, stop_scroll
from automation.keyboard_controller import press_key, type_text
from automation.mouse_controller import move_relative
from automation.executor import Executor
import pyautogui

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
        # MOVE MOUSE (PIXEL BASED)
        # -------------------------
        if intent == "move_mouse":

            distance = command.get("entities", {}).get("distance")
            move_direction = command.get("entities", {}).get("direction", "right")

            if distance:
                move_relative(distance, move_direction)
                print(f"Moved mouse {distance}px {move_direction}")

        # -------------------------
        # CLICK ACTION
        # -------------------------
        elif intent == "click":

            click_type = command.get("entities", {}).get("click_type", "left")
            entity = command.get("entities", {}).get("object")

            # If object exists → OCR click
            if entity:

                img = capture_screen()
                detections = self.ocr.read_text(img)

                pos = find_text(detections, entity)

                if pos:
                    x, y = pos
                    pyautogui.moveTo(x, y, duration=0.4)

                    from automation.mouse_controller import perform_click
                    perform_click(click_type)

                    print(f"{click_type} clicked '{entity}' at {pos}")
                else:
                    print(f"Could not find '{entity}' on screen")

            # Else → generic click
            else:
                from automation.mouse_controller import perform_click
                perform_click(click_type)

                print(f"Performed {click_type} click")
        

        # -------------------------
        # GOTO TEXT (HOVER ONLY)
        # -------------------------
        elif intent == "goto":

            target = command.get("entities", {}).get("object")

            if target:
                img = capture_screen()
                detections = self.ocr.read_text(img)

                pos = find_text(detections, target)

                if pos:
                    pyautogui.moveTo(pos[0], pos[1], duration=0.5)
                    print(f"Hovered on '{target}'")

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

        # -------------------------
        # TYPE ACTION
        # -------------------------
        elif intent == "type":

            text_to_type = command.get("entities", {}).get("text")

            # fallback: extract from raw text properly
            if not text_to_type:
                raw = command.get("text", "").strip()

                # remove only the first occurrence of "type"
                parts = raw.lower().split("type", 1)

                if len(parts) > 1:
                    text_to_type = parts[1].strip()
                else:
                    text_to_type = raw

            if text_to_type:
                type_text(text_to_type)
                print(f"Typed: {text_to_type}")

        # -------------------------
        # KEY PRESS ACTION
        # -------------------------

        elif intent == "press":

            key = command.get("entities", {}).get("key")

            if not key:
                raw = command.get("text", "").lower()

                if "enter" in raw:
                    key = "enter"
                elif "escape" in raw:
                    key = "esc"
                elif "tab" in raw:
                    key = "tab"

            if key:
                press_key(key)
                print(f"Pressed: {key}")
        
        # -------------------------
        # OPEN APP
        # -------------------------
        elif intent == "open_app":

            app_name = command.get("entities", {}).get("app")

            if app_name:
                Executor().open_app(app_name)
                print(f"Opening {app_name}")