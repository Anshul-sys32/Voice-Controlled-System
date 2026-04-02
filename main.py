from audio import MicrophoneStream, VoiceActivityDetector, SpeechBuffer
from speech_to_text.transcriber import Transcriber
import numpy as np
from nlp.command_parser import CommandParser
from planner.action_planner import ActionPlanner

mic = MicrophoneStream()
vad = VoiceActivityDetector()
buffer = SpeechBuffer()
parser = CommandParser()
stt = Transcriber()
planner = ActionPlanner()   # ← create planner instance

print("Listening...")

mic.start()

while True:

    chunk = mic.read()
    speech = vad.is_speech(chunk)

    result = buffer.process(chunk, speech)

    if result is not None:

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

            planner.execute(command)   # ← correct call