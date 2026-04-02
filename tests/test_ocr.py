from vision.screen_capture import capture_screen
from vision.ocr_reader import OCRReader
from vision.text_locator import find_text
import numpy as np

ocr = OCRReader()

img = capture_screen()
img = np.array(img)

detections = ocr.read_text(img)

pos = find_text(detections, "Terminal")

print("Position:", pos)