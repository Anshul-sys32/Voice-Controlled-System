import webrtcvad
import numpy as np

class WebRTCVAD:
    def __init__(self, aggressiveness=2, sample_rate=16000):
        """
        aggressiveness: 0 (least aggressive) → 3 (most aggressive)
        """
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = sample_rate
        self.frame_duration = 30  # ms (10, 20, or 30)
        self.frame_size = int(sample_rate * self.frame_duration / 1000)

    def is_speech(self, audio_chunk):
        """
        audio_chunk: float32 numpy array (16kHz)
        """
        if len(audio_chunk) < self.frame_size:
            return False

        # convert float32 → int16 PCM
        pcm = (audio_chunk * 32768).astype(np.int16).tobytes()

        try:
            return self.vad.is_speech(pcm[: self.frame_size * 2], self.sample_rate)
        except Exception:
            return False