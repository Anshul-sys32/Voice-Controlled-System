import numpy as np

class VoiceActivityDetector:
    def __init__(self, threshold=0.01):
        self.threshold = threshold

    def is_speech(self, audio_chunk):
        energy = np.sqrt(np.mean(np.square(audio_chunk)))
        return energy > self.threshold