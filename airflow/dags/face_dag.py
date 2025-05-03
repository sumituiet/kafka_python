from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from datetime import datetime
import os

IMAGE_PATH = 'image.jpg'
CFG_PATH = 'yolov3-face.cfg'
WEIGHTS_PATH = 'yolov3-wider_16000.weights'

default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    dag_id="yolo_face_detection_venv",
    schedule_interval=None,
    catchup=False,
    tags=["face_detection"],
    default_args=default_args,
) as dag:

    def load_image():
        import cv2
        import numpy as np
        import pickle

        img = cv2.imread(IMAGE_PATH)
        with open('/tmp/image.pkl', 'wb') as f:
            pickle.dump(img, f)

    def preprocess_image():
        import cv2
        import numpy as np
        import pickle

        with open('/tmp/image.pkl', 'rb') as f:
            img = pickle.load(f)

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True, crop=False)
        with open('/tmp/blob.pkl', 'wb') as f:
            pickle.dump(blob, f)

    def run_yolo():
        import cv2
        import numpy as np
        import pickle

        with open('/tmp/blob.pkl', 'rb') as f:
            blob = pickle.load(f)

        net = cv2.dnn.readNetFromDarknet(CFG_PATH, WEIGHTS_PATH)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())

        detections = []
        h, w = 416, 416  # assuming resized image

        for output in outputs:
            for detection in output:
                confidence = detection[4]
                if confidence > 0.5:
                    center_x, center_y, width, height = (
                        detection[0] * w,
                        detection[1] * h,
                        detection[2] * w,
                        detection[3] * h
                    )
                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)
                    detections.append([x, y, int(width), int(height), float(confidence)])

        with open('/tmp/detections.pkl', 'wb') as f:
            pickle.dump(detections, f)

    def postprocess():
        import pickle
        import cv2
        import numpy as np

        with open('/tmp/image.pkl', 'rb') as f:
            img = pickle.load(f)
        with open('/tmp/detections.pkl', 'rb') as f:
            detections = pickle.load(f)

        boxes = []
        confidences = []

        for det in detections:
            x, y, w, h, conf = det
            boxes.append([x, y, w, h])
            confidences.append(conf)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in indices.flatten():
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite('/tmp/output.jpg', img)
        print("Saved output to /tmp/output.jpg")

    reqs = ["opencv-python", "numpy", "pickle5", "dlib"]

    task1 = PythonVirtualenvOperator(
        task_id="load_image",
        python_callable=load_image,
        requirements=reqs,
        system_site_packages=False,
    )

    task2 = PythonVirtualenvOperator(
        task_id="preprocess_image",
        python_callable=preprocess_image,
        requirements=reqs,
        system_site_packages=False,
    )

    task3 = PythonVirtualenvOperator(
        task_id="run_yolo",
        python_callable=run_yolo,
        requirements=reqs,
        system_site_packages=False,
    )

    task4 = PythonVirtualenvOperator(
        task_id="postprocess",
        python_callable=postprocess,
        requirements=reqs,
        system_site_packages=False,
    )

    task1 >> task2 >> task3 >> task4