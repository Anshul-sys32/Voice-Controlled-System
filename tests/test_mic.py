import argparse
import sys
from pathlib import Path

import numpy as np
import sounddevice as sd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio.mic_input import MicrophoneStream


def run_mic_test(duration=3.0):
    if duration <= 0:
        raise ValueError("duration must be greater than zero")

    print(f"Recording from the default microphone for {duration:g} seconds...")
    stream = MicrophoneStream()
    chunks = []
    target_samples = int(stream.samplerate * duration)
    started = False

    try:
        stream.start()
        started = True
        sample_count = 0
        while sample_count < target_samples:
            chunk = stream.read()
            chunks.append(chunk)
            sample_count += len(chunk)
    finally:
        if started:
            stream.stop()

    recording = np.concatenate(chunks)[:target_samples]
    if recording.size == 0 or not np.isfinite(recording).all():
        raise RuntimeError("Microphone returned no valid audio samples")

    rms = float(np.sqrt(np.mean(np.square(recording))))
    peak = float(np.max(np.abs(recording)))
    print(f"Captured {recording.size} samples; RMS: {rms:.4f}, peak: {peak:.4f}")
    if peak == 0:
        print("Warning: the recording is silent. Check the selected microphone and input level.")

    print("Playing the recording through the default output device...")
    sd.play(recording, samplerate=stream.samplerate)
    sd.wait()
    return recording


def main():
    parser = argparse.ArgumentParser(description="Record and play back microphone input")
    parser.add_argument(
        "--duration",
        type=float,
        default=3.0,
        help="recording duration in seconds (default: 3)",
    )
    args = parser.parse_args()
    run_mic_test(args.duration)


if __name__ == "__main__":
    main()