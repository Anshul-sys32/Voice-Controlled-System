from .whisper_stt import WhisperSTT
from .confidence_filter import ConfidenceFilter

class Transcriber:

    def __init__(self):
        self.stt = WhisperSTT()
        self.filter = ConfidenceFilter()
    
    def process(self, audio):

        text, conf = self.stt.transcribe(audio)

        print("WHISPER TEXT:", text)
        print("CONFIDENCE:", conf)

        if not self.filter.is_valid(conf):
            print("Rejected by confidence filter")
            return None

        return text

    # def process(self, audio):

    #     text, conf = self.stt.transcribe(audio)

    #     if not self.filter.is_valid(conf):
    #         return None

    #     return text