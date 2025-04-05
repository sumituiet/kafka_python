# consumer.py
from kafka import KafkaConsumer
import json
from database import insert_face_data

# Set up Kafka consumer
consumer = KafkaConsumer(
    'Faces',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Waiting for messages... Press CTRL+C to exit.\n")

try:
    for msg in consumer:
        data = msg.value
        print("\nReceived JSON:")
        print(json.dumps(data, indent=2))
        
        # Insert into MongoDB
        insert_face_data(data)

except KeyboardInterrupt:
    print("\nConsumer stopped.")
finally:
    consumer.close()