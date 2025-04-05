from fastapi import FastAPI
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import threading
import json

app = FastAPI()

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "chat"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Store received messages (in-memory queue)
messages = []

# Kafka Consumer in Background Thread
def consume_messages():
    global messages
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    for msg in consumer:
        messages.append(msg.value)  # Store messages

# Run consumer in a separate thread
threading.Thread(target=consume_messages, daemon=True).start()

# API to Send Message
@app.post("/send")
def send_message(content: str, sender: str):
    try:
        message = {"sender": sender, "content": content}
        producer.send(TOPIC_NAME, message)
        producer.flush()
        return {"status": "Message sent", "message": message}
    except KafkaError as e:
        return {"error": str(e)}

# API to Fetch Received Messages
@app.get("/receive")
def get_messages():
    global messages
    latest_messages = messages.copy()
    messages.clear()  # Clear after sending
    return {"messages": latest_messages}
