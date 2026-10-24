import re
from utils.nlp_model import nlp


class EntityExtractor:

    def extract(self, text: str, intent: str = None):

        doc = nlp(text.lower())
        entities = {}

        # -------------------------
        # MOVE (distance + direction)
        # -------------------------
        if intent == "move_mouse":

            match = re.search(r"move (\d+)\s*(.*)", text.lower())

            if match:
                entities["distance"] = int(match.group(1))
                raw_direction = match.group(2).strip().lower()

                raw_direction = raw_direction.replace("pixels", "").replace("pixel", "")
                raw_direction = raw_direction.replace(".", "").strip()

                direction_map = {
                    "top right": "top-right",
                    "top left": "top-left",
                    "bottom right": "bottom-right",
                    "bottom left": "bottom-left",
                    "up": "up",
                    "top": "up",
                    "down": "down",
                    "bottom": "down",
                    "left": "left",
                    "right": "right",
                }

                # find best match
                for key in direction_map:
                    if key in raw_direction:
                        entities["direction"] = direction_map[key]
                        break

            # fallback (if no number given)
            if "direction" not in entities:
                if "up" in text:
                    entities["direction"] = "up"
                    entities["distance"] = entities.get("distance", 50)
                elif "down" in text:
                    entities["direction"] = "down"
                    entities["distance"] = entities.get("distance", 50)

            return entities

        # -------------------------
        # OPEN APP
        # -------------------------
        if intent == "open_app":

            app = text.lower().replace("open", "").replace("launch", "").strip()

            # remove punctuation
            app = re.sub(r"[^\w\s-]", "", app).strip()

            if app:
                entities["app"] = app
            return entities
        
        # -------------------------
        # CLOSE APP
        # -------------------------
        if intent == "close_app":

            app = text.lower().replace("close", "").replace("exit", "").strip()
            app = re.sub(r"[^\w\s-]", "", app).strip()

            if app:
                entities["app"] = app

            return entities

        # -------------------------
        # TYPE TEXT
        # -------------------------
        if intent == "type":

            parts = text.lower().split("type", 1)

            if len(parts) > 1:
                entities["text"] = parts[1].strip()
            else:
                entities["text"] = text

            return entities

        # -------------------------
        # PRESS KEY
        # -------------------------
        if intent == "press":

            for word in text.lower().split():
                if word in ["enter", "esc", "escape", "tab", "space"]:
                    entities["key"] = "esc" if word == "escape" else word

            return entities

        # -------------------------
        # SCROLL
        # -------------------------
        if intent == "scroll":

            if "up" in text:
                entities["direction"] = "up"
            elif "down" in text:
                entities["direction"] = "down"
                
        # -------------------------
        # CLICK TYPE
        # -------------------------
        if intent == "click":

            text_lower = text.lower()

            if "double" in text_lower:
                entities["click_type"] = "double"
            elif "right" in text_lower:
                entities["click_type"] = "right"
            elif "middle" in text_lower:
                entities["click_type"] = "middle"
            else:
                entities["click_type"] = "left"

        # -------------------------
        # GOTO / CLICK (object detection)
        # -------------------------
        if intent in ["click", "goto", "scroll"]:

            noun_chunks = [chunk.text for chunk in doc.noun_chunks]

            if noun_chunks:
                candidate = noun_chunks[-1].strip().lower()

                invalid_objects = [
                    "click",
                    "double click",
                    "right click",
                    "left click"
                ]

                if candidate not in invalid_objects:
                    entities["object"] = candidate
            else:
                for token in doc:
                    if token.pos_ in ["NOUN", "PROPN"]:
                        if token.text not in ["click", "scroll"]:
                            entities["object"] = token.text
        return entities