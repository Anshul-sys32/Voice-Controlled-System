from audio import MicrophoneStream, VoiceActivityDetector, SpeechBuffer, RNNoiseReducer
from speech_to_text.transcriber import Transcriber
import numpy as np
from nlp import CommandParser
from planner import ActionPlanner

mic = MicrophoneStream()
vad = VoiceActivityDetector()
buffer = SpeechBuffer()
nr = RNNoiseReducer()

parser = CommandParser()
stt = Transcriber()
planner = ActionPlanner()

print("Listening...")

mic.start()

while True:
    try:
        chunk = mic.read()

        energy = np.sqrt(np.mean(np.square(chunk)))

        if energy > 0.003:
            clean_chunk = nr.reduce_noise(chunk)
        else:
            clean_chunk = chunk
        is_speech = vad.is_speech(clean_chunk)

        result = buffer.process(clean_chunk, is_speech)

        if result is not None:
            print("\n--- Speech Detected ---")
            print("Speech length:", len(result))
            print("Speech amplitude:", np.max(np.abs(result)))

            if len(result) < 16000:
                print("Too short, skipping")
                continue

            print("Processing speech...")
            text = stt.process(result)
            print("RAW TEXT:", text)

            if text:
                print("You said:", text)
                command = parser.parse(text)
                print("Command:", command)
                planner.execute(command)

    except KeyboardInterrupt:
        print("\nStopping...")
        mic.stop()
        break

    except Exception as e:
        print("Error:", e)