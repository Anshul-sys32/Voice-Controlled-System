from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import EntityExtractor


class CommandParser:

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()

    def parse(self, text):

        intent = self.intent_classifier.classify(text)
        entities = self.entity_extractor.extract(text)

        return {
            "intent": intent,
            "entities": entities,
            "text": text
        }