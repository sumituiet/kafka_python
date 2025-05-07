import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from kafka import KafkaProducer
from PIL import Image
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone
from kafka import KafkaConsumer
app = FastAPI()

# Kafka configuration
KAFKA_TOPIC = "heatmap"
KAFKA_SERVER = os.getenv('KAFKA_SERVER')

# Airflow configuration
AIRFLOW_BASE_URL = os.getenv('AIRFLOW_BASE_URL')
AIRFLOW_LOGIN = {
    "username": os.getenv('USERNAME'),
    "password": os.getenv('PASSWORD')
}
DAG_ID = "object_detection_single_task"

def compress_image_bytes(file: UploadFile, quality=50) -> bytes:
    """Compress uploaded image and return bytes."""
    img = Image.open(file.file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=quality, optimize=True)
    return img_bytes.getvalue()

def send_to_kafka(image_bytes: bytes,topic:str=KAFKA_TOPIC):
    """Send compressed image to Kafka."""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: v
    )
    future = producer.send(topic, image_bytes)
    producer.flush(timeout=10)
    return future.get(timeout=10)  # Wait for confirmation

def trigger_airflow_dag(dag_id):
    """Trigger Airflow DAG using session authentication."""
    session = requests.Session()
    login_url = f"{AIRFLOW_BASE_URL}/login/"
    
    # Step 1: Get CSRF token
    resp = session.get(login_url)
    if "csrf_token" in resp.text:
        soup = BeautifulSoup(resp.text, "html.parser")
        token = soup.find("input", {"name": "csrf_token"})["value"]
        AIRFLOW_LOGIN["csrf_token"] = token

    resp = session.post(login_url, data=AIRFLOW_LOGIN)
    if "DAGs" not in resp.text:
        raise Exception("Airflow login failed!")

    # Step 2: Trigger DAG
    trigger_url = f"{AIRFLOW_BASE_URL}/api/v1/dags/{dag_id}/dagRuns"
    dt = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
    payload = {
        "conf": {},
        "dag_run_id": f"run_{requests.utils.default_headers()['User-Agent'][-4:]}",
        "logical_date": dt.strftime('%Y-%m-%dT%H:%M:%S.') + f'{int(dt.microsecond / 1000):03d}Z',
        # "data_interval_start": "2025-04-30T07:22:58.104Z",
        # "data_interval_end": "2025-04-30T07:22:58.104Z",
        "note": "triggered via API"
    }
    headers = {"Content-Type": "application/json"}
    response = session.post(trigger_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"DAG trigger failed: {response.text}")
    return response.json()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), dag_id: str = DAG_ID):
    try:
        KAFKA_TOPIC = "image_blob_topic" if dag_id == 'object_detection_single_task' else 'heatmap'
        RESULT_TOPIC = "results_topic"

        # Compress image and send to Kafka
        compressed_bytes = compress_image_bytes(file)
        kafka_result = send_to_kafka(compressed_bytes, KAFKA_TOPIC)

        # Trigger Airflow DAG
        airflow_result = trigger_airflow_dag(dag_id)

        # Wait for DAG run to complete and read JSON from Kafka result topic
        consumer = KafkaConsumer(
            RESULT_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='result_consumer_group',
            value_deserializer=lambda x: x.decode('utf-8')
        )

        for message in consumer:
            consumer.close()
            return {
                "status": "success",
                "kafka": {
                    "topic": kafka_result.topic,
                    "partition": kafka_result.partition,
                    "offset": kafka_result.offset,
                },
                "airflow": airflow_result,
                "result": message.value
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/trigger-test-kafka-dag/")
def trigger_test_kafka_dag():
    """Trigger the test_kafka_in_virtualenv_dag DAG via Airflow API and wait for Kafka output."""
    try:
        session = requests.Session()
        login_url = f"{AIRFLOW_BASE_URL}/login/"
        
        # Get CSRF token
        resp = session.get(login_url)
        if "csrf_token" in resp.text:
            soup = BeautifulSoup(resp.text, "html.parser")
            token = soup.find("input", {"name": "csrf_token"})["value"]
            AIRFLOW_LOGIN["csrf_token"] = token

        resp = session.post(login_url, data=AIRFLOW_LOGIN)
        if "DAGs" not in resp.text:
            raise HTTPException(status_code=500, detail="Airflow login failed!")

        # Trigger DAG
        dag_id = "test_kafka_in_virtualenv_dag"
        trigger_url = f"{AIRFLOW_BASE_URL}/api/v1/dags/{dag_id}/dagRuns"
        payload = {
            "dag_run_id": f"run_{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.')}",
            "logical_date": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.') + f'{int(datetime.now(timezone.utc).microsecond / 1000):03d}Z',
            "note": "Test trigger for Kafka virtualenv DAG"
        }

        headers = {"Content-Type": "application/json"}
        response = session.post(trigger_url, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"DAG trigger failed: {response.text}")

        # Wait for Kafka output
        consumer = KafkaConsumer(
            'kafka_test',
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='test_kafka_group',
            value_deserializer=lambda x: x.decode('utf-8')
        )

        for message in consumer:
            consumer.close()
            return {
                "status": "DAG triggered and Kafka message received",
                "dag_id": dag_id,
                "kafka_message": message.value
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))