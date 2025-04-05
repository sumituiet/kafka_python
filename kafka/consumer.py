from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'chat',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: v.decode('utf-8')
)

print("Waiting for messages...")
for msg in consumer:
    print(f"Received: {msg.value}")
