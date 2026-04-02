import sounddevice as sd
import numpy as np
import queue


class MicrophoneStream:
    def __init__(self, samplerate=16000, blocksize=1024, channels=1):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.audio_queue = queue.Queue()

        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            blocksize=self.blocksize,
            dtype="float32",
            callback=self.callback
        )

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata[:, 0].copy())

    def start(self):
        self.stream.start()

    def read(self):
        return self.audio_queue.get(timeout=2)

    def stop(self):
        self.stream.stop()
        self.stream.close()