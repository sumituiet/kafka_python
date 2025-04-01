import cv2
import numpy as np
import json
from kafka import KafkaConsumer

# Initialize Kafka consumer
consumer = KafkaConsumer(
    "media-stream",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    # group_id="media-consumers"
)

while True:
    for msg in consumer:
        data = json.loads(msg.value.decode('utf-8'))
        timestamp = data["timestamp"]
        
        # Decode the video frame (convert hex back to bytes, then decode image)
        frame_bytes = bytes.fromhex(data["video_chunk"])
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Decode audio similarly (you’d use an audio library to play or process audio)
        audio_bytes = bytes.fromhex(data["audio_chunk"])
        
        # Here you could synchronize and display the frame with audio playback
        cv2.imshow("Video Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
consumer.close()
cv2.destroyAllWindows()
