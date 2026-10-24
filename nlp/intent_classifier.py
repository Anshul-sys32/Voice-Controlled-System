from utils.nlp_model import nlp
import re

class IntentClassifier:

    def classify(self, text: str):

        text = re.sub(r"[^\w\s]", "", text.lower())
        doc = nlp(text)

        tokens = [token.lemma_ for token in doc]

        if "open" in tokens or "launch" in tokens:
            return "open_app"

        if "close" in tokens or "exit" in tokens:
            return "close_app"

        if "click" in tokens:
            return "click"

        if "scroll" in tokens:
            return "scroll"

        if "type" in tokens or "write" in tokens:
            return "type"

        if "press" in tokens or "hit" in tokens:
            return "press"
        
        if "stop" in tokens:
            return "stop"
        
        if "move" in tokens:
            return "move_mouse"

        if "goto" in text or "go to" in text:
            return "goto"

        return "unknown"