import cv2

def draw_detections(image, detections):

    for det in detections:
        bbox = det["bbox"]
        text = det["text"]
        conf = det["confidence"]

        x1, y1 = map(int, bbox[0])
        x3, y3 = map(int, bbox[2])

        cv2.rectangle(image, (x1, y1), (x3, y3), (0,255,0), 2)

        label = f"{text} ({conf:.2f})"
        cv2.putText(
            image,
            label,
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            1,
            cv2.LINE_AA
        )

    return image