from faster_whisper import WhisperModel
import os
import numpy as np
import soundfile as sf
import librosa

class WhisperSTT:

    def __init__(self):

        model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "faster-whisper-small.en"
        )

        print("Loading Whisper model...")

        self.model = WhisperModel(
            model_path,
            device="cuda",
            compute_type="float16"
        )

        print("Whisper model loaded")

    def transcribe(self, audio):

        audio = np.asarray(audio, dtype=np.float32)

        # Handle different audio formats correctly
        if audio.dtype == np.int16:
            audio = audio.astype(np.float32) / 32768.0
        elif audio.dtype == np.int32:
            audio = audio.astype(np.float32) / 2147483648.0
        else:
            audio = audio.astype(np.float32)

        # Ensure valid range for Whisper
        max_val = np.max(np.abs(audio))
        if max_val > 1:
            audio = audio / max_val

        print("Audio dtype:", audio.dtype)
        print("Audio min:", np.min(audio))
        print("Audio max:", np.max(audio))

        segments, info = self.model.transcribe(
            audio,
            language="en",
            beam_size=1,
            best_of=1,
            temperature=0,
            vad_filter=False
        )

        text = ""
        confidences = []

        for seg in segments:
            text += seg.text
            confidences.append(seg.avg_logprob)

        if len(confidences) == 0:
            return "", -10

        confidence = sum(confidences) / len(confidences)

        return text.strip(), confidence