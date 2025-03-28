from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8') if isinstance(v, str) else v
)

def send_message(topic, message):
    producer.send(topic, message)
    producer.flush()
    print(f"Sent: {message}")

send_message('chat', 'Hello, Kafka with Kraft!')
