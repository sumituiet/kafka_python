## Apache Airflow Documentation for Face Detection and Feature Extraction Pipelines
## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Purpose](#2-purpose)
- [3. System Requirements](#3-system-requirements)
- [4. Access Credentials](#4-access-credentials)
- [5. Project Structure](#5-project-structure)
- [6. Environment Setup](#6-environment-setup)
- [7. How the DAGs Work](#7-how-the-dags-work)
- [8. Detailed DAG Documentation](#8-detailed-dag-documentation)
  - [8.1 face_detection.py](#81-face_detectionpy)
  - [8.2 detect_faces_and_features.py](#82-detect_faces_and_featurespy)
  - [8.3 face_dag.py](#83-face_dagpy)
  - [8.4 heatmaps_kafka.py](#84-heatmaps_kafkapy)
  - [8.5 example_dag.py](#85-example_dagpy)
  - [8.6 sahi.py](#86-sahipy)
- [9. Kafka Integration](#9-kafka-integration)
- [10. Logging and Monitoring](#10-logging-and-monitoring)
- [11. Common Issues & Troubleshooting](#11-common-issues--troubleshooting)
- [12. Glossary](#12-glossary)
- [13. Testing Procedures](#13-testing-procedures)
- [14. Error Handling Strategies](#14-error-handling-strategies)
- [15. Performance Considerations](#15-performance-considerations)
- [16. API Integration](#16-api-integration)
  - [16.1 Triggering DAGs via FastAPI Service](#161-triggering-dags-via-fastapi-service)
  - [16.2 End-to-End Workflow](#162-end-to-end-workflow)
  - [16.3 Configuration and Environment Variables](#163-configuration-and-environment-variables)
  - [16.4 Implementation Details](#164-implementation-details)
  - [16.5 Using the API Service](#165-using-the-api-service)
  - [16.6 Best Practices for Using the API Service](#166-best-practices-for-using-the-api-service)

## 1. Introduction
This repository contains a collection of Apache Airflow DAGs used in a real-time face detection and crowd monitoring system. The pipeline orchestrates various tasks like frame ingestion from Kafka, running deep learning inference (YOLO, emotion, mask detection), and publishing the results.

Airflow plays a key role in:
- Orchestrating complex workflows
- Scheduling and triggering detection jobs
- Running image processing in isolated environments
- Managing dependencies between tasks

The system includes a FastAPI service (`api.py`) that provides endpoints for uploading images, triggering DAGs, and retrieving results, creating a complete end-to-end pipeline from image upload to result delivery.

## 2. Purpose
The goal of this documentation is to:
- Explain how each DAG contributes to the system
- Clarify dependencies and input/output
- Enable easy onboarding for new developers and contributors
- Provide setup, monitoring, and troubleshooting steps
- Ensure code consistency and reliability

## 3. System Requirements
- **Python**: 3.8 or later  
- **Apache Airflow**: 2.5 or later  
- **Kafka Cluster** (already hosted on Redback)  
- **Libraries**: Pillow, OpenCV, SAHI, Ultralytics, kafka-python, numpy, dlib
- **Storage**: Sufficient disk space for model weights (~300MB)
- **Memory**: Minimum 4GB RAM recommended for YOLO inference

## 4. Access Credentials
You can access the Airflow UI using:

- **URL**: http://redback.it.deakin.edu.au:8888  
- **Username**: `project_4`  
- **Password**: `TYojTPXO14gtRoFbkNVYUQ9y2cBagSwsCWyvbqs_REA`  

The FastAPI service has these credentials configured as environment variables and handles authentication with the Airflow API automatically.

## 5. Project Structure
```bash
project/
├── airflow/
│   └── dags/
│       ├── face_detection.py
│       ├── detect_faces_and_features.py
│       ├── face_dag.py
│       ├── heatmaps_kafka.py
│       ├── example_dag.py
│       └── sahi.py
├── api/
│   └── api.py              # FastAPI service for image upload and DAG triggering
```

## 6. Environment Setup
Airflow operators use Python virtual environments via PythonVirtualenvOperator. Required model weights and config files are downloaded dynamically at runtime.

**Required ENV_VARS for Airflow DAGs**
```bash
KAFKA_BOOTSTRAP_SERVER=redback.it.deakin.edu.au:9092
YOLO_CFG=/tmp/yolov4-face.cfg
YOLO_WEIGHTS=/tmp/yolov4-face.weights
MASK_MODEL=/tmp/mask_detector.model
AGE_PROTO=/tmp/age_deploy.prototxt
AGE_MODEL=/tmp/age_net.caffemodel
EMOTION_MODEL=/tmp/emotion-ferplus-8.onnx
```

For the heatmaps and SAHI-based object detection:
```bash
HEATMAP_TOPIC=heatmap
HEATMAP_DETECTED_TOPIC=heatmap_detected
RESULTS_TOPIC=results_topic
YOLO_WEIGHTS_PATH=/tmp/yolov8n.pt
```

**Required ENV_VARS for FastAPI Service**
```bash
KAFKA_SERVER=redback.it.deakin.edu.au:9092
AIRFLOW_BASE_URL=http://redback.it.deakin.edu.au:8888
USERNAME=project_4
PASSWORD=TYojTPXO14gtRoFbkNVYUQ9y2cBagSwsCWyvbqs_REA
```

Model URLs are embedded in the DAGs and downloaded using urllib if not already present.

## 7. How the DAGs Work
Each DAG represents a specific pipeline, some DAGs are standalone and others work together in a sequence. They operate on API-triggered runs through the FastAPI service. Common steps include:

- Consuming images from Kafka topics
- Running detection/inference (YOLO, age, emotion, mask)
- Annotating images
- Publishing JSON + image results to Kafka

The DAGs utilize task dependencies to ensure operations are performed in the correct sequence. For model-based operations, the workflow typically includes:
1. Download model weights (if not present)
2. Consume data from Kafka
3. Process data using models
4. Publish results back to Kafka

## 8. Detailed DAG Documentation
### 8.1 face_detection.py
- **DAG ID**: face_feature_extraction

- **Trigger**: API-triggered via FastAPI service

- **Operator**: PythonVirtualenvOperator

#### API Trigger Details:
- **Method**: POST to FastAPI endpoint `/upload/`
- **Parameters**: Image file upload with `dag_id` parameter set to "face_feature_extraction"
- **Process**: 
  - Image is compressed and sent to face_images Kafka topic
  - DAG is triggered via Airflow API with session authentication
  - Results are retrieved from face_results Kafka topic

#### What it does:
- Downloads missing models
- Subscribes to face_images topic
- Runs detection for face, age, mask, emotion
- Publishes result JSON to face_results
- Requirements: opencv-python, numpy, kafka-python, Pillow

#### Error Handling:
- Downloads missing models only if needed
- Sets consumer timeout to handle Kafka connection issues
- Uses confidence thresholds to filter reliable predictions

### 8.2 detect_faces_and_features.py
- **DAG ID**: face_feature_extraction

- **Purpose**: Main pipeline for face detection and feature extraction

- **Trigger**: API-triggered via FastAPI service (same as face_detection.py)

- **Input Topic**: face_images

- **Output Topic**: face_results

#### Flow:
- Downloads required models if missing
- Initializes neural networks for face detection, age estimation, mask detection, and emotion analysis
- Consumes images from Kafka
- Processes each image through multiple models
- Publishes detailed JSON results with bounding boxes, age, mask status, and emotion data
- Uses environment variables for configuration

#### Requirements:
- opencv-python
- numpy
- kafka-python
- Pillow

### 8.3 face_dag.py
- **DAG ID**: tutorial

- **Purpose**: Basic template DAG showing Airflow configuration

- **Trigger**: Manual

- **Structure**: Minimal DAG showing standard configuration options

#### Configuration:
- Standard Airflow options (owner, retries, email settings)
- Catchup enabled
- No actual tasks defined in this template
- Good for understanding basic Airflow DAG structure
- Use as a starting point for new DAGs

### 8.4 heatmaps_kafka.py
- **DAG ID**: process_heatmap_images

- **Purpose**: Slice-based object detection using YOLOv8 and SAHI

- **Trigger**: API-triggered via FastAPI service

- **Input Topic**: heatmap

- **Output Topics**: results_topic, heatmap_detected

#### API Trigger Details:
- **Method**: POST to FastAPI endpoint `/upload/`
- **Parameters**: Image file upload with `dag_id` parameter set to "process_heatmap_images"
- **Process**: 
  - Image is compressed and sent to heatmap Kafka topic
  - DAG is triggered via Airflow API with session authentication
  - Results are retrieved from results_topic Kafka topic

#### Flow:
- Pulls image from Kafka
- Runs get_sliced_prediction with SAHI
- Publishes both JSON results and annotated image
- Uses slicing technique for better detection of small objects
- Sets confidence threshold at 0.3

#### Technical Details:
- Processes images as 256x256 slices with 20% overlap
- Converts SAHI prediction format to standardized JSON
- Visualizes predictions on original image
- Publishes both data types to separate topics

### 8.5 example_dag.py
- **DAG ID**: example_dag

- **Purpose**: A simple test DAG to demonstrate sequential task execution

- **Trigger**: Manual

#### Tasks:
- print_hello - Logs a greeting
- wait_for_a_while - Sleeps for 5 seconds
- Good for: Testing DAG scheduling, dependencies, and logs

A separate DAG with ID `yolo_face_detection_venv` is also present in this file, which demonstrates:
- Loading a test image
- Preprocessing for YOLO 
- Running YOLOv3 for face detection
- Postprocessing + drawing boxes
- Uses pickle to pass data between tasks
- Good for understanding YOLO output formats

### 8.6 sahi.py
- **Purpose**: Integration helper for SAHI (Slicing Aided Hyper Inference)

- **Functionality**: 
  - Provides utilities for sliced object detection
  - Integrates with YOLOv8 models
  - Helps with better detection of small objects in images

- **Usage**:
  - Imported by heatmaps_kafka.py
  - Handles slicing logic and prediction visualization
  - Formats predictions for consistent output

## 9. Kafka Integration

Airflow DAGs interface directly with Kafka topics using the kafka-python package:

- KafkaConsumer: Reads image blobs from topics
- KafkaProducer: Sends JSON metadata and image bytes to output topics

### Example Topics:
- face_images
- face_results  
- heatmap
- results_topic
- heatmap_detected

### Connection Settings:
- Default bootstrap server: redback.it.deakin.edu.au:9092
- Consumer timeout: 10000ms (10 seconds)
- Auto offset reset: 'earliest'

### Data Formats:
- Images: Raw binary (JPEG bytes)
- Results: JSON format with standardized fields
- Annotated images: Raw binary (JPEG bytes with visual annotations)

## 10. Logging and Monitoring

- All Airflow logs are available in the UI > DAG > Task Logs
- Important checkpoints (e.g., image received, model loaded, JSON result sent) are logged using print()
- You can add more structured logs using Python's logging module if needed
- When debugging, check:
  - Airflow task instance logs
  - Kafka consumer group offsets
  - Model download success/failure messages

## 11. Common Issues & Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| DAG not appearing in UI | File not in `dags/` or syntax error | Check file name and Airflow scheduler logs |
| Kafka timeout | No messages in topic | Use Kafka UI to confirm topic state |
| Operator failure due to deps | Missing Python packages in `requirements` | Add them explicitly in the DAG operator |
| Model path not found | Weight files not downloaded | Ensure URL is correct and `os.path.exists()` logic works |
| Tasks stuck in queued state | Resource constraints or scheduler issues | Check Airflow worker logs and executor status |
| YOLO inference errors | Incompatible model format | Verify model version matches code expectations |
| API upload fails | File too large or incorrect format | Check file size and format before upload |
| Session authentication fails | Incorrect credentials or CSRF token | Verify environment variables for API service |
| Missing response from Kafka | Consumer timeout before processing completes | Increase consumer timeout in FastAPI or implement polling |

## 12. Glossary

| Term | Description |
|------|-------------|
| DAG | Directed Acyclic Graph, represents a pipeline |
| Task | A single step in the DAG, defined by an operator |
| Kafka | Distributed event streaming platform |
| SAHI | Slicing Aided Hyper Inference library for object detection |
| YOLO | You Only Look Once, object detection model |
| Virtualenv | Isolated Python environment per operator task |
| NMS | Non-Maximum Suppression, technique to reduce duplicate detections |
| Confidence | Probability score of detection accuracy |
| FastAPI | Python web framework for building APIs with automatic input validation |
| CSRF Token | Cross-Site Request Forgery token, used for secure authentication |
| Session Authentication | Authentication method using cookies and server-side sessions |
| API Trigger | Method to start DAG runs via REST API calls |

## 13. Testing Procedures

### Local Testing:
1. **Verify DAG Syntax**: Run `python -c "from airflow.models import DagBag; d = DagBag()"`
2. **Test Individual Tasks**: Use Airflow's test command: `airflow tasks test [dag_id] [task_id] [execution_date]`
3. **Test Kafka Connectivity**: Use simple consumer/producer scripts before running the full DAG
4. **Test API Triggers**: Use curl or Postman to verify API trigger functionality

### Test Data:
- Store sample images in a designated test directory
- Create test Kafka topics with `-test` suffix

### Validation:
- Check that detections match expected objects
- Verify bounding box coordinates are reasonable
- Ensure emotion and age classifications are consistent
- Confirm API-triggered DAGs execute as expected
## 13. Testing Procedures

### Local Testing:
1. **Verify DAG Syntax**: Run `python -c "from airflow.models import DagBag; d = DagBag()"`
2. **Test Individual Tasks**: Use Airflow's test command: `airflow tasks test [dag_id] [task_id] [execution_date]`
3. **Test Kafka Connectivity**: Use simple consumer/producer scripts before running the full DAG
4. **Test FastAPI Service**: Use the `/trigger-test-kafka-dag/` endpoint to verify end-to-end connectivity

### FastAPI Testing:
1. **Unit Testing**: Test image compression function and Kafka producer separately
2. **Integration Testing**: Use test images to verify the complete upload-process-result flow
3. **Error Handling**: Confirm proper error responses for invalid inputs or connection issues

### Test Data:
- Store sample images in a designated test directory
- Create test Kafka topics with `-test` suffix

### Validation:
- Check that detections match expected objects
- Verify bounding box coordinates are reasonable
- Ensure emotion and age classifications are consistent
- Confirm API responses contain all expected fields


## 14. Error Handling Strategies

### Retry Mechanism:
- Most DAGs use `retries: 1` with a 5-minute delay
- Consider increasing for production environments

### Error Catching:
- Kafka consumer timeouts prevent indefinite blocking
- Model download errors are handled with existence checks
- Confidence thresholds filter low-quality detections
- API trigger failures provide detailed error responses

### Recovery:
- Failed tasks can be manually rerun from the Airflow UI
- Consider implementing dead-letter queues for failed messages
- Add explicit error handling in Python callable functions
- Use API status checks to confirm successful DAG initiation

## 15. Performance Considerations

### Scaling:
- YOLO inference is CPU-intensive; consider GPU support for production
- SAHI slicing increases accuracy but adds processing time
- Use multiple workers for parallel task execution

### Resource Allocation:
- Increase memory for large image processing
- Monitor CPU utilization during inference
- Consider batching for higher throughput

### Optimization:
- Reduce slice overlap in SAHI for faster processing
- Adjust confidence thresholds based on application needs
- Pre-download models during deployment rather than runtime
- Implement rate limiting for API triggers to prevent system overload

## 16. API Integration

### 16.1 Triggering DAGs via FastAPI Service
The system provides a FastAPI web service (`api.py`) that serves as the primary interface for uploading images and triggering Airflow DAGs. This service handles:
- Image upload and compression
- Kafka message publication
- Airflow DAG triggering via session authentication
- Result retrieval from Kafka output topics

#### Available DAGs for Triggering
The following DAGs can be triggered via the API:
- `object_detection_single_task` (default)
- `face_feature_extraction`
- `process_heatmap_images`
- `test_kafka_in_virtualenv_dag` (test endpoint only)

#### API Endpoints

1. **Image Upload and Processing**
   - **Endpoint**: `/upload/`
   - **Method**: POST
   - **Parameters**:
     - `file`: Image file upload (required)
     - `dag_id`: DAG identifier to trigger (optional, defaults to `object_detection_single_task`)
   - **Actions**:
     - Compresses the uploaded image
     - Sends image to appropriate Kafka topic based on DAG ID
     - Triggers the specified Airflow DAG
     - Waits for and returns processing results from result topic

2. **Test Kafka DAG Trigger**
   - **Endpoint**: `/trigger-test-kafka-dag/`
   - **Method**: POST
   - **Actions**:
     - Triggers the test_kafka_in_virtualenv_dag
     - Waits for response in kafka_test topic
     - Returns status and kafka message

#### Authentication Flow
The service uses Airflow's session-based authentication:
1. Sends GET request to Airflow's login page to retrieve CSRF token
2. Authenticates with username/password and CSRF token
3. Uses the authenticated session for DAG triggering API calls

#### Airflow DAG Trigger Process
```python
# Example payload for triggering a DAG
payload = {
    "conf": {},
    "dag_run_id": f"run_{requests.utils.default_headers()['User-Agent'][-4:]}",
    "logical_date": dt.strftime('%Y-%m-%dT%H:%M:%S.') + f'{int(dt.microsecond / 1000):03d}Z',
    "note": "triggered via API"
}
```

### 16.2 End-to-End Workflow

1. Client uploads an image via the `/upload/` endpoint with optional `dag_id` parameter
2. The FastAPI service:
   - Compresses the image using PIL
   - Sends the compressed image to the appropriate Kafka topic:
     - `image_blob_topic` for object detection DAG
     - `heatmap` for other DAGs
   - Triggers the specified Airflow DAG via session authentication
   - Waits for results from the `results_topic` Kafka topic
3. The triggered Airflow DAG:
   - Consumes the image from the specified Kafka topic
   - Processes the image (face detection, feature extraction, etc.)
   - Publishes results back to the designated output topic
4. The API service returns the complete result to the client

#### Example Response
```json
{
  "status": "success",
  "kafka": {
    "topic": "heatmap",
    "partition": 0,
    "offset": 42
  },
  "airflow": {
    "conf": {},
    "dag_id": "process_heatmap_images",
    "dag_run_id": "run_abcd",
    "end_date": null,
    "execution_date": "2025-05-19T12:00:00+00:00",
    "external_trigger": true,
    "start_date": "2025-05-19T12:00:00+00:00",
    "state": "running"
  },
  "result": "{\"detections\": [{\"type\": \"person\", \"confidence\": 0.92, \"bbox\": [23, 45, 67, 89]}]}"
}
```

### 16.3 Configuration and Environment Variables

The API service relies on several environment variables:
- `KAFKA_SERVER`: Kafka bootstrap server address
- `AIRFLOW_BASE_URL`: Base URL for the Airflow web server
- `USERNAME`: Airflow username for authentication
- `PASSWORD`: Airflow password for authentication

### 16.4 Implementation Details

#### Image Processing
- Uploaded images are compressed to JPEG format with quality=50
- RGB conversion is applied if needed
- Compressed images are serialized to bytes before Kafka transmission

#### Authentication Method
The API uses session-based authentication with CSRF token instead of Basic Auth:
1. Retrieves CSRF token from Airflow login page
2. Submits login credentials along with CSRF token
3. Uses the authenticated session cookie for subsequent API calls

#### Airflow DAG Trigger URL
```
{AIRFLOW_BASE_URL}/api/v1/dags/{dag_id}/dagRuns
```

#### Error Handling
The API implements comprehensive error handling:
- HTTP exceptions with appropriate status codes (500 for internal errors)
- Detailed error messages in response
- Timeout handling for Kafka operations (10 seconds)

### 16.5 Using the API Service

#### Example API Call Using curl
```bash
curl -X POST http://your-fastapi-service-url/upload/ \
  -F "file=@your_image.jpg" \
  -F "dag_id=face_feature_extraction"
```

#### Example API Call Using Python Requests
```python
import requests

url = "http://your-fastapi-service-url/upload/"
files = {"file": open("your_image.jpg", "rb")}
data = {"dag_id": "face_feature_extraction"}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result)
```

#### Testing the Kafka DAG Integration
```bash
curl -X POST http://your-fastapi-service-url/trigger-test-kafka-dag/
```

### 16.6 Best Practices for Using the API Service

- Ensure images are in common formats (JPEG, PNG)
- Keep image sizes reasonable to avoid performance issues
- Use the appropriate `dag_id` for your processing needs:
  - Use `object_detection_single_task` for basic object detection
  - Use `process_heatmap_images` for SAHI-based detection
  - Use `face_feature_extraction` for face analysis
- Implement timeouts and retries in client applications
- Handle potential delays between DAG triggering and result availability
- Monitor the API service logs for debugging issues# Apache Airflow Documentation for Face Detection and Feature Extraction Pipelines