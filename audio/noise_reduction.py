import numpy as np
import resampy
from pyrnnoise import RNNoise

class RNNoiseReducer:
    def __init__(self, input_rate=16000, rnnoise_rate=48000):
        self.input_rate = input_rate
        self.rnnoise_rate = rnnoise_rate
        self.model = RNNoise(sample_rate=rnnoise_rate)

    def reduce_noise(self, audio_chunk):
        DEBUG_RNNOISE = False
        try:
            if audio_chunk is None or len(audio_chunk) == 0:
                return audio_chunk

            if audio_chunk.dtype != np.float32:
                audio_chunk = audio_chunk.astype(np.float32)

            upsampled = resampy.resample(audio_chunk, self.input_rate, self.rnnoise_rate)

            frame_size = 480
            processed = []

            for i in range(0, len(upsampled), frame_size):
                frame = upsampled[i:i + frame_size]

                if len(frame) < frame_size:
                    frame = np.pad(frame, (0, frame_size - len(frame)))

                denoised = self.model.denoise_frame(frame)

                if denoised is None:
                    denoised = frame

                processed.append(denoised)

            if len(processed) == 0:
                return audio_chunk

            processed = np.concatenate(processed)

            downsampled = resampy.resample(processed, self.rnnoise_rate, self.input_rate)

            return downsampled.astype(np.float32)
        except Exception as e:
            if DEBUG_RNNOISE:
                print("RNNoise Error:", e)
            return audio_chunk