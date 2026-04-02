import numpy as np
from pyrnnoise import RNNoise


class RNNoiseReducer:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.model = RNNoise(sample_rate=self.sample_rate)

    def reduce_noise(self, audio_chunk):
        """
        Accepts numpy float32 array
        Must be 480 samples long
        """

        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32)

        audio_chunk = audio_chunk.flatten()

        # RNNoise requires exactly 480 samples
        if len(audio_chunk) != 480:
            return audio_chunk

        denoised = self.model.denoise_frame(audio_chunk)

        return np.array(denoised, dtype=np.float32)
