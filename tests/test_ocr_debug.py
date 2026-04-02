import cv2
import numpy as np
from vision.screen_capture import capture_screen
from vision.ocr_reader import OCRReader
from vision.ocr_debug_viewer import draw_detections

ocr = OCRReader()

img = capture_screen()
img = np.array(img)
detections = ocr.read_text(img)

debug_img = draw_detections(img, detections)

cv2.imshow("OCR Debug", debug_img)
cv2.waitKey(0)
cv2.destroyAllWindows()