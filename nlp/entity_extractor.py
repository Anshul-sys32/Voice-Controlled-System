from utils.nlp_model import nlp


class EntityExtractor:

    def extract(self, text: str):

        doc = nlp(text)

        entities = {}

        for token in doc:

            if token.pos_ in ["NOUN", "PROPN"]:
                entities["object"] = token.text

        return entities