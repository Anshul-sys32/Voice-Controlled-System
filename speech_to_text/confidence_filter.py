class ConfidenceFilter:

    def __init__(self, threshold=-1.5):
        self.threshold = threshold

    def is_valid(self, confidence):
        return confidence > self.threshold