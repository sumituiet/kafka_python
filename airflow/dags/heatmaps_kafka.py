import os
import io
import json
import numpy as np
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Environment variables for Kafka and model path
ENV_VARS = {
    'KAFKA_BOOTSTRAP_SERVER': os.getenv('KAFKA_BOOTSTRAP_SERVER', 'redback.it.deakin.edu.au:9092'),
    'HEATMAP_TOPIC': 'heatmap',
    'HEATMAP_DETECTED_TOPIC': 'heatmap_detected',
    'RESULTS_TOPIC': 'results_topic',
    'YOLO_WEIGHTS_PATH': '/tmp/yolov8n.pt'
}

with DAG(
    dag_id='process_heatmap_images',
    default_args=default_args,
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    def process_heatmap_images():
        import os
        import io
        import json
        import numpy as np
        from kafka import KafkaConsumer, KafkaProducer
        from sahi import AutoDetectionModel
        from sahi.predict import get_sliced_prediction
        from sahi.utils.cv import visualize_object_predictions
        from PIL import Image

        # Retrieve environment variables
        kafka_server = os.getenv('KAFKA_BOOTSTRAP_SERVER')
        heatmap_topic = os.getenv('HEATMAP_TOPIC')
        heatmap_detected_topic = os.getenv('HEATMAP_DETECTED_TOPIC')
        results_topic = os.getenv('RESULTS_TOPIC')
        weights_path = os.getenv('YOLO_WEIGHTS_PATH')

        # Set up Kafka consumer to read from the heatmap topic
        consumer = KafkaConsumer(
            heatmap_topic,
            bootstrap_servers=[kafka_server],
            auto_offset_reset='earliest',
            consumer_timeout_ms=10000,
        )

        # Consume the latest image message
        for msg in consumer:
            img_bytes = msg.value
            break
        else:
            raise RuntimeError('No image blob received from Kafka topic')

        # Load image from bytes
        img = Image.open(io.BytesIO(img_bytes))

        # Load the YOLOv8 model using SAHI
        model = AutoDetectionModel.from_pretrained(
            model_type='yolov8',
            model_path=weights_path,
            confidence_threshold=0.3,
            device='cpu'
        )

        # Perform sliced prediction
        result = get_sliced_prediction(
            image=img,
            detection_model=model,
            slice_height=256,
            slice_width=256,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2,
        )

        # Construct JSON results
        preds = [
            {
                'category_id': int(o.category.id),
                'category_name': o.category.name,
                'score': float(o.score.value),
                'bbox': {
                    'x_min': o.bbox.minx,
                    'y_min': o.bbox.miny,
                    'x_max': o.bbox.maxx,
                    'y_max': o.bbox.maxy
                }
            }
            for o in result.object_prediction_list
        ]
        json_payload = json.dumps(preds).encode('utf-8')

        # Annotate the image with predictions
        img_np = np.array(img)
        annotated_img = visualize_object_predictions(
            image=img_np,
            object_prediction_list=result.object_prediction_list
        )

        # Convert the annotated image to bytes
        annotated_pil = Image.fromarray(annotated_img)
        buf = io.BytesIO()
        annotated_pil.save(buf, format='JPEG')
        annotated_bytes = buf.getvalue()

        # Set up Kafka producer to send the results
        producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda v: v  # Send raw bytes
        )
        producer.send(results_topic, json_payload)
        producer.send(heatmap_detected_topic, annotated_bytes)
        producer.flush()

    # Define the task using PythonVirtualenvOperator
    process_heatmap_task = PythonVirtualenvOperator(
        task_id='process_heatmap_images',
        python_callable=process_heatmap_images,
        requirements=['sahi', 'ultralytics', 'kafka-python', 'Pillow'],
        system_site_packages=True,
        env_vars=ENV_VARS
    )

    process_heatmap_task
