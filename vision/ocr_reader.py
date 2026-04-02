import easyocr
import cv2
import numpy as np

class OCRReader:
    def __init__(self):
        print("Loading OCR model...")
        self.reader = easyocr.Reader(['en'], gpu=True)
        print("OCR model loaded")

    def read_text(self, image):
        """
        Returns detected text with bounding boxes
        """
        results = self.reader.readtext(image)

        detections = []

        for bbox, text, confidence in results:
            detections.append({
                "text": text,
                "confidence": confidence,
                "bbox": bbox
            })

        return detections