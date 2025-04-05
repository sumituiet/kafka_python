# producer.py
from kafka import KafkaProducer
import json
import cv2
import time
from models import detect_faces_from_frame

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'Faces'
video_path = 'crowd.mp4'  # Replace with your actual video path
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps / 3)  # Pick frame every 1/3 second

frame_id = 0
sent_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % frame_interval == 0:
        result = detect_faces_from_frame(frame, frame_id)
        producer.send(topic, result)
        print(f"✅ Sent Frame {frame_id}: {result['total_faces']} faces")
        sent_count += 1

    frame_id += 1

cap.release()
producer.flush()
print(f"\n✅ Finished processing. Total frames sent: {sent_count}")