import cv2
import pyaudio
import json
from kafka import KafkaProducer
import time

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Capture video frames using OpenCV
cap = cv2.VideoCapture(0)  # or a video file

# Audio setup (example using PyAudio)
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Encode frame as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        continue
    frame_bytes = buffer.tobytes()
    
    # Read audio chunk
    audio_chunk = stream.read(1024)
    
    # Create a message with frame and audio data, plus a timestamp for synchronization
    message = {
        "timestamp": time.time(),
        "video_chunk": frame_bytes.hex(),  # hex encode binary data
        "audio_chunk": audio_chunk.hex()
    }
    
    # Send message to Kafka topic (e.g., 'media-stream')
    producer.send("media-stream", json.dumps(message).encode('utf-8'))
    producer.flush()  # optionally flush at intervals

cap.release()
stream.stop_stream()
stream.close()
audio.terminate()
