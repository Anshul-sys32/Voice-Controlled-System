import numpy as np


class SpeechBuffer:
    def __init__(self, silence_limit=10, min_chunks=15):
        """
        silence_limit = silent frames before speech ends
        min_chunks = minimum frames required to treat as valid speech
        """
        self.silence_limit = silence_limit
        self.min_chunks = min_chunks

        self.buffer = []
        self.silence_frames = 0
        self.recording = False

    def process(self, audio_chunk, is_speech):

        if is_speech:
            self.recording = True
            self.silence_frames = 0
            self.buffer.append(audio_chunk)

        elif self.recording:
            self.silence_frames += 1
            self.buffer.append(audio_chunk)

            if self.silence_frames > self.silence_limit:

                # check speech length
                if len(self.buffer) < self.min_chunks:
                    # discard noise
                    self.buffer = []
                    self.recording = False
                    self.silence_frames = 0
                    return None

                speech = np.concatenate(self.buffer)

                self.buffer = []
                self.recording = False
                self.silence_frames = 0

                return speech

        return None