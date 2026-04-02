import numpy as np

def find_text(detections, target):
    """
    Find coordinates of target text
    """

    target = target.lower()

    for det in detections:
        text = det["text"].lower()

        if target in text:
            bbox = det["bbox"]

            x = int((bbox[0][0] + bbox[2][0]) / 2)
            y = int((bbox[0][1] + bbox[2][1]) / 2)

            return (x, y)

    return None