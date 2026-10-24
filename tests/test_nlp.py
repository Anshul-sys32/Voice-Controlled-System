from nlp.intent_classifier import IntentClassifier

classifier = IntentClassifier()

while True:
    text = input("Command: ")
    intent = classifier.classify(text)

    print("Intent:", intent)