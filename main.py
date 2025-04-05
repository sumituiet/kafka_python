import cv2
import numpy as np
import json

# Load YOLOv3 face detection model
net = cv2.dnn.readNetFromDarknet("yolov3-face.cfg", "yolov3-wider_16000.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Define the function to detect faces and return JSON
def detect_faces(image_path, confidence_threshold=0.5):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    ln = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(ln)

    boxes = []
    confidences = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            confidence = float(scores[0])
            if confidence > confidence_threshold:
                center_x, center_y, width, height = (detection[0:4] * [w, h, w, h]).astype("int")
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)
                boxes.append([int(x), int(y), int(width), int(height)])
                confidences.append(confidence)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)
    final_faces = []

    for idx in indices.flatten():
        box = boxes[int(idx)]
        final_faces.append({
            "face_id": int(idx),
            "bounding_box": {
                "x": int(box[0]),
                "y": int(box[1]),
                "width": int(box[2]),
                "height": int(box[3])
            },
            "confidence": round(float(confidences[int(idx)]), 2)
        })

    result = {
        "total_faces": int(len(final_faces)),
        "faces": final_faces
    }

    return result

# Example usage
if __name__ == "__main__":
    output_json = detect_faces("group.jpg")
    print(json.dumps(output_json, indent=2))