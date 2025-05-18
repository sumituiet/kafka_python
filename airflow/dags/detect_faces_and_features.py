from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from datetime import datetime, timedelta
import os

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

ENV_VARS = {
    'KAFKA_BOOTSTRAP_SERVER': os.getenv('KAFKA_BOOTSTRAP_SERVER', 'redback.it.deakin.edu.au:9092'),
    'IMAGE_TOPIC': 'face_images',
    'RESULTS_TOPIC': 'face_results',
    'YOLO_CFG': '/tmp/yolov4-face.cfg',
    'YOLO_WEIGHTS': '/tmp/yolov4-face.weights',
    'MASK_MODEL': '/tmp/mask_detector.model',
    'AGE_PROTO': '/tmp/age_deploy.prototxt',
    'AGE_MODEL': '/tmp/age_net.caffemodel',
    'EMOTION_MODEL': '/tmp/emotion-ferplus-8.onnx'
}

def detect_faces_and_features():
    import os
    import cv2
    import io
    import json
    import numpy as np
    import urllib.request
    from PIL import Image
    from kafka import KafkaConsumer, KafkaProducer

    def download_if_missing(url, path):
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)

    # Download required models
    download_if_missing("https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/yolov4-face.cfg", os.getenv('YOLO_CFG'))
    download_if_missing("https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx", os.getenv('YOLO_WEIGHTS'))
    download_if_missing("https://github.com/chandrikadeb7/Face-Mask-Detection/raw/master/mask_detector.model", os.getenv('MASK_MODEL'))
    download_if_missing("https://github.com/smahesh29/Gender-and-Age-Detection/raw/master/age_deploy.prototxt", os.getenv('AGE_PROTO'))
    download_if_missing("https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel", os.getenv('AGE_MODEL'))
    download_if_missing("https://github.com/onnx/models/raw/main/validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx", os.getenv('EMOTION_MODEL'))

    face_net = cv2.dnn.readNetFromDarknet(os.getenv('YOLO_CFG'), os.getenv('YOLO_WEIGHTS'))
    age_net = cv2.dnn.readNetFromCaffe(os.getenv('AGE_PROTO'), os.getenv('AGE_MODEL'))
    mask_net = cv2.dnn.readNet(os.getenv('MASK_MODEL'))
    emotion_net = cv2.dnn.readNetFromONNX(os.getenv('EMOTION_MODEL'))

    layer_names = face_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in face_net.getUnconnectedOutLayers()]

    age_labels = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    emotion_labels = ['neutral', 'happy', 'sad', 'surprise', 'anger']

    consumer = KafkaConsumer(
        os.getenv('IMAGE_TOPIC'),
        bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVER')],
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000
    )

    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVER'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for msg in consumer:
        img = Image.open(io.BytesIO(msg.value)).convert('RGB')
        frame = np.array(img)
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        face_net.setInput(blob)
        outputs = face_net.forward(output_layers)

        results = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6:
                    center_x, center_y, box_w, box_h = [int(detection[i] * w if i % 2 == 0 else detection[i] * h) for i in range(4)]
                    x = max(center_x - box_w // 2, 0)
                    y = max(center_y - box_h // 2, 0)
                    face = frame[y:y+box_h, x:x+box_w]

                    face_blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (78.426337, 87.768914, 114.895848), swapRB=False)
                    
                    # Age Estimation
                    age_net.setInput(face_blob)
                    age_preds = age_net.forward()
                    age = age_labels[age_preds[0].argmax()]

                    # Mask Detection
                    mask_blob = cv2.dnn.blobFromImage(face, 1.0, (224, 224), (104, 117, 123), swapRB=True)
                    mask_net.setInput(mask_blob)
                    mask_result = mask_net.forward()
                    wearing_mask = bool(np.argmax(mask_result[0]) == 0)

                    # Emotion Analysis
                    emotion_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, (64, 64), (0,), swapRB=True, crop=False)
                    emotion_net.setInput(emotion_blob)
                    emotion_preds = emotion_net.forward()
                    emotion = emotion_labels[np.argmax(emotion_preds[0])]

                    results.append({
                        'bbox': [x, y, box_w, box_h],
                        'age': age,
                        'mask': wearing_mask,
                        'emotion': emotion,
                        'confidence': float(confidence)
                    })

        producer.send(os.getenv('RESULTS_TOPIC'), {
            'detections': results,
            'frame_size': {'width': w, 'height': h}
        })
        producer.flush()
        break

    consumer.close()

with DAG(
    dag_id='face_feature_extraction',
    default_args=default_args,
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    detect_faces_task = PythonVirtualenvOperator(
        task_id='detect_faces_and_features',
        python_callable=detect_faces_and_features,
        requirements=[
            'opencv-python', 'numpy', 'kafka-python', 'Pillow'
        ],
        system_site_packages=True,
        env_vars=ENV_VARS
    )

    detect_faces_task
