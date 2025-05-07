import os
import io
import sys
import base64
import requests
from PIL import Image
from kafka import KafkaProducer

def compress_image(image_path, quality=50):
    """
    Compresses an image and returns it as a bytes object.
    Lower quality means more compression.
    """
    with Image.open(image_path) as img:
        # Convert image to RGB if it's not (e.g., PNG)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Save to an in-memory bytes buffer with JPEG compression
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=quality, optimize=True)
        return img_bytes.getvalue()

def send_image_blob(image_path):
    # Compress the image
    compressed_image_bytes = compress_image(image_path, quality=50)  # Adjust quality as needed

    # Set up Kafka producer with size allowance 
    producer = KafkaProducer(
        bootstrap_servers='redback.it.deakin.edu.au:9092',
        value_serializer=lambda v: v,  # Send raw bytes
    )

    # Send the compressed image blob
    future = producer.send('heatmap', compressed_image_bytes)

    # Logging result
    future.add_callback(lambda m: print(f"Sent to {m.topic}, partition {m.partition}, offset {m.offset}"))
    future.add_errback(lambda e: print(f"Error sending: {e}"))

    producer.flush(timeout=10)

    # After sending the image, trigger the Airflow DAG
    # trigger_airflow_dag()

def trigger_airflow_dag():
    """
    Triggers the 'object_detection_single_task' DAG via Airflow's REST API.
    """
    airflow_api_url = 'http://redback.it.deakin.edu.au:8888/api/v1/dags/object_detection_single_task/dagRuns'
    # Replace these with your actual Airflow credentials
    airflow_username = 'project_4'
    airflow_password = 'TYojTPXO14gtRoFbkNVYUQ9y2cBagSwsCWyvbqs_REA'

    # Optional: You can pass a unique run_id or conf if needed
    payload = {
        "conf": {}
    }

    try:
        response = requests.post(
            airflow_api_url,
            auth=(airflow_username, airflow_password)
        )

        if response.status_code == 200:
            print("Successfully triggered the Airflow DAG.")
        else:
            print(f"Failed to trigger the DAG. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error triggering the Airflow DAG: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_image_blob_to_kafka.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    send_image_blob(image_path)
