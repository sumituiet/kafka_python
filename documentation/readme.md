# Kafka Python Documentation - Table of Contents

## Introduction
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start-guide)
- [Use Cases](#use-cases)

## Installation
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting Installation](#troubleshooting-installation)

## Core Concepts
- [Kafka Architecture Overview](#kafka-architecture-overview)
- [Producer-Consumer Model](#producer-consumer-model)
- [Topics and Partitions](#topics-and-partitions)
- [Message Delivery Semantics](#message-delivery-semantics)

## Getting Started
- [Basic Setup](#basic-setup)
- [Simple Producer Example](#simple-producer-example)
- [Simple Consumer Example](#simple-consumer-example)
- [Configuration Options](#configuration-options)

## API Reference
- [Producer API](#producer-api)
- [Consumer API](#consumer-api)
## Advanced Usage
- [Serialization and Deserialization](#serialization-and-deserialization)
- [Error Handling and Retry Mechanisms](#error-handling-and-retry-mechanism)
- [Performance Tuning](#performance-tuning)
- [Monitoring and Metrics](#monitoring-and-metrics)
## Deployment
- [Production Best Practices](#production-best-practices)
- [Scaling Considerations](#scaling-considerations)
- [Containerization with Docker](#containerization-with-docker)
- [Cloud Deployment Options](#cloud-deployment-options)

## Examples
- [Basic Examples](#basic-examples)
-  [Real World Scenarios](#real-world-scenarios)
-  [Integration with Other Systems](#integration-with-other-systems)
-  [Batch Processing](#batch-processing)
-  [Stream Processing](#stream-processing)

## Contributing
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Pull Request process](#pull-request-process)

## Troubleshooting
- [Common Issues](#common-issues)
- [Debugging Tips](#debugging-tips)
- [FAQ](#faq)

## Appendix
- [Glossary](#glossary)
- [Additonal Resources](#additional-resources)
- [Version History](#version-history)



# Project Overview
## Kafka Python Backend for Crowd Monitoring
The **Kafka Python Backend** is a critical component of the Crowd Monitoring system designed to process images and video frames for face detection using a messaging architecture. This backend infrastructure leverages Apache Kafka for efficient message handling, FastAPI for lightweight API endpoints, and YOLOv3 for accurate face detection in crowd monitoring applications.

## Purpose
The main goals of this project are:
1. Process images and video frames for crowd monitoring applications
2. Implement a producer-consumer architecture for distributed message processing
3. Utilize Apache Kafka to handle high-throughput message streams efficiently 
4. Provide REST API endpoints through FastAPI for system integration
5. Apply YOLOv3 for accurate face detection in crowd analysis

## Architecture Overview
This project implements a messaging-based architecture with:
- **Kafka Message Broker**: Handles communication between components for crowd monitoring data
- **FastAPI Service**: Provides REST API endpoints for sending and receiving detection results
- **YOLOv3 Processing**: Performs face detection on crowd footage
- **MongoDB Integration**: Stores face detection results for crowd analysis
- **Background Processing**: Runs Kafka consumer in a separate thread for continuous operation

## Technical Components
- **app.py**: FastAPI application with Kafka integration and REST endpoints
- **model.py**: YOLOv3 face detection implementation with JSON result formatting
- **producer.py**: Face detection code for producing messages to Kafka
- **consumer.py**: Kafka consumer for processing face detection results and storing in MongoDB

## System Requirements
- **Python**: 3.10 or higher
- **Kafka**: Running in Docker
- **Package Manager**: uv 0.6 or higher
- **Web Framework**: FastAPI
- **Container Platform**: Docker & Docker Compose

## Setup & Deployment
The system can be deployed using Docker Compose for simplified setup of the Kafka server and related services. A virtual environment is managed through the uv tool, with documentation available through FastAPI's built-in Swagger UI.

---
[Table of Contents](:/e603cea36b144275b9d1db73c2452e51) | [Next: Key Features](:/407760a71f504e3aa2270f122abacf6e)

# Quick Start Guide

This guide will help you quickly set up and run the Kafka Python Backend for your Crowd Monitoring project.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or higher
- Docker and Docker Compose
- uv 0.6 or higher

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/sumituiet/kafka_python.git
   cd kafka_python
   ```

2. **Start Kafka and related services**
    ```bash
	docker-compose up -d
    ```
3. **Create and activate a virtual environment using uv**
    ```bash
    uv venv
    ```
4. **Activate the virtual environemnt (Windows/macOS/Linux)**
    ```bash
    source .venv/bin/activate
    ```
5. **(Optional) Install uv inside the environment if not already available**
    ```bash
    pip install uv
    ```

## Running the Application
1. **Start the FastAPI server**
   ```bash
   fastapi dev app.py
   ```
 The server will start at http://127.0.0.1:8000
Access the API documentation

Open your browser and navigate to http://127.0.0.1:8000/docs
This interactive documentation allows you to test all API endpoints

 ## Testing Face Detection

1. Send a test message

- Use the /send endpoint to publish a test message to Kafka
    Example :
```bash
  {
  "content": "process_image",
  "sender": "test_client"
  }
```

2. Process an image

  - Place test images in your project directory
```bash
from model import detect_faces
results = detect_faces("path/to/image.jpg")
print(results)
```

3. Retreive processed images

- Use the /receive endpoint to get messages from the Kafka consumer.

 ## Monitoring 

- Check your terminal for consumer output
- MongoDB will store all processed face detection results
- Use tools like Kafka UI (available at http://localhost:8080 if using the default Docker setup) to monitor Kafka topics

# Key Features
The Kafka Python Backend with Face Detection offers specialized features designed for real-time face detection and messaging:

## Core Features

### Real-time Message Processing
- Asynchronous communication through Kafka messaging system
- In-memory message queue for temporary storage
- Background thread consumer for continuous message processing
- Efficient message handling with JSON serialization

### YOLOv3 Face Detection
- Advanced face detection using YOLOv3 neural network
- Pre-trained model with optimized configuration
- Model architecture defined in yolov3.cfg configuration file
- Configurable confidence thresholds (default: 0.5)
- Support for both static images and video frames
- Detailed face location data with bounding boxes
- Face confidence scoring for detection quality assessment

### FastAPI Integration
- High-performance RESTful API endpoints
- JSON-based message format for seamless data exchange
- Simple `/send` endpoint for message production
- `/receive` endpoint for retrieving processed messages
- Automatic cleanup of delivered messages

### Kafka-Powered Architecture
- Producer-consumer pattern for distributed processing
- Reliable message delivery with Kafka guarantees
- Configurable broker settings
- Topic-based message organization
- JSON serialization/deserialization for structured data

## Additional Features

### Structured Face Detection Results
- Frame identification for video processing
- Total face count in each processed image
- Detailed face records with unique IDs
- Precise bounding box coordinates (x, y, width, height)
- Confidence scores for each detected face

### Data Persistence
- MongoDB integration for storing face detection results
- Structured data format for efficient querying
- Persistent storage of detection results

### Flexible Processing Options
- Support for file-based image processing
- Frame-by-frame video processing capabilities
- Customizable confidence thresholds
- Non-maximum suppression for removing duplicate detections

### Developer-Friendly Implementation
- Modular code organization
- Clear separation of concerns
- Easily extendable architecture
- Simple configuration of Kafka brokers and topics

---
[Project Overview](:/2c760b6d4d4a4c9bb4ab1bb2938566e6) | [Table of Contents](:/e603cea36b144275b9d1db73c2452e51) | [Use Cases](:/387aff55a3b14a4e87e8a65b455deaee)

# Use Cases

This document outlines the primary use cases for the Kafka Python Backend with YOLOv3 face detection in crowd monitoring applications.

## Crowd Analysis

### Real-time Crowd Density Monitoring
- **Description**: Monitor crowd density in public spaces by detecting and counting faces in video streams.
- **Implementation**: Security camera feeds are processed frame-by-frame using the YOLOv3 model, with face counts published to Kafka topics for real-time monitoring.
- **Benefit**: Allows security personnel to identify potential overcrowding situations before they become dangerous.

### Facility Capacity Management
- **Description**: Track facility occupancy levels to ensure compliance with capacity regulations.
- **Implementation**: The system processes entrance and exit camera feeds, using face detection to count individuals entering and leaving the facility.
- **Benefit**: Helps venues maintain safe occupancy levels and comply with safety regulations.

## Security Applications

### Unauthorized Access Detection
- **Description**: Monitor restricted areas for unauthorized personnel.
- **Implementation**: The system continuously processes camera feeds from restricted areas, sending alerts when faces are detected in zones that should be vacant.
- **Benefit**: Enhances security by providing immediate notification when restricted zones are breached.

### Anomalous Behavior Detection
- **Description**: Identify unusual crowd movements or gatherings.
- **Implementation**: By analyzing the number and distribution of detected faces over time, the system can recognize sudden changes in crowd patterns.
- **Benefit**: Helps security teams respond proactively to potentially problematic situations.

## Marketing and Analytics

### Customer Traffic Analysis
- **Description**: Analyze customer traffic patterns in retail environments.
- **Implementation**: Face detection data from store cameras is processed to generate heatmaps of customer presence throughout business hours.
- **Benefit**: Provides retailers with valuable insights for optimizing store layouts and staffing.

### Engagement Measurement
- **Description**: Measure audience engagement with displays or presentations.
- **Implementation**: By detecting faces oriented toward displays, the system can estimate attention levels and dwell time.
- **Benefit**: Helps marketing teams evaluate the effectiveness of visual merchandising and advertisements.

## Event Management

### Queue Management
- **Description**: Monitor queue lengths and waiting times.
- **Implementation**: Camera feeds focused on queuing areas are processed to count faces, with data used to estimate wait times.
- **Benefit**: Improves customer experience by allowing staff to open additional service points when queues grow too long.

### Event Attendance Tracking
- **Description**: Track attendance at events or specific areas.
- **Implementation**: The system processes video from entry points, using YOLOv3 face detection to count unique attendees.
- **Benefit**: Provides accurate attendance metrics for event organizers and sponsors.

## Health and Safety

### Social Distancing Compliance
- **Description**: Monitor adherence to social distancing guidelines.
- **Implementation**: By analyzing the spatial distribution of detected faces, the system can identify areas where people are clustered too closely together.
- **Benefit**: Helps enforce health protocols and reduce transmission risks in public spaces.

### Emergency Evacuation Management
- **Description**: Support safe evacuations during emergencies.
- **Implementation**: Real-time face detection helps track crowd movement during evacuations, identifying bottlenecks or areas where people might be trapped.
- **Benefit**: Assists emergency responders in prioritizing rescue efforts and improving evacuation procedures.

# Installation

This guide will walk you through the complete installation process for the Kafka Python Backend with YOLOv3 face detection.

## Requirements

### System Requirements
- **Operating System**: Linux (recommended), macOS, or Windows
- **RAM**: Minimum 8GB (16GB recommended for production)
- **Storage**: At least 10GB free disk space
- **CPU**: Multi-core processor (recommended for video processing)

### Software Prerequisites
- **Python**: Version 3.10 or higher
- **Docker**: Latest stable version
- **Docker Compose**: Latest stable version
- **uv**: Version 0.6 or higher (Python package manager)
- **Git**: For repository cloning

### Network Requirements
- Port 9092 available for Kafka broker
- Port 8000 available for FastAPI service
- Port 27017 available for MongoDB (if using the database)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sumituiet/kafka_python.git
cd kafka_python
```
### 2. Start Docker Services
**Start Kafka, ZooKeeper, and MongoDB using Docker Compose:**
```bash
docker-compose up -d
```
### 3. Verify Services are running
```bash
docker-compose ps
```
### 4. Setup Python Environment
**Create and activate virtual environment using uv:**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
**Install required dependencies:**
```bash
uv install
```
## Environment Configuration
### 1. Configure Kafka Connection ###
**By default, the application connects to Kafka at localhost:9092. To modify this:
Edit app.py, producer.py, and consumer.py to update the KAFKA_BROKER variable:**
```bash
# Default
KAFKA_BROKER = "localhost:9092"

# Example for custom configuration
KAFKA_BROKER = "your-kafka-server:9092"
```

### 2. Configure Topic Names ###
**Update Kafka Topics needed**
**In app.py (default)**
```bash
TOPIC_NAME = "faces"
```

In consumer.py (default)
**Consumer topic for 'Faces'.**

### 3.Configure YOLOv3 Parameters ###
Ensure the following model files are placed in the appropriate directory (e.g., models/):

- `yolov3-face.cfg – Defines the YOLOv3 model architecture`

- `yolov3-wider_16000.weights – Pre-trained weights file for face detection`
```bash
# Default confidence threshold is 0.5
# To modify, change function calls:
results = detect_faces("image.jpg", confidence_threshold=0.4) 
 # More sensitive
 ```

#  Troubleshooting Installation

##  Docker Issues

- **Problem**: Docker services not starting  
  **Solution**:  
  - Check if the Docker daemon is running:  
    ```bash
    docker info
    ```
  - Ensure required ports are free:  
    ```bash
    netstat -tulpn | grep <port>
    ```

- **Problem**: Kafka not accessible  
  **Solution**:  
  - View Kafka logs:  
    ```bash
    docker-compose logs kafka
    ```
  - Check if Kafka is exposed on the correct port (`9092` by default)

---

##  Python Environment Issues

- **Problem**: `uv` command not found  
  **Solution**:  
  - Install `uv` using pip:  
    ```bash
    pip install uv
    ```

- **Problem**: Package installation failures  
  **Solution**:  
  - Check your Python version (recommended: Python 3.8+)  
  - Update `uv` if already installed:  
    ```bash
    pip install -U uv
    ```

---

##  YOLOv3 Model Issues

- **Problem**: Model files not found  
  **Solution**:  
  - Make sure the following files are in the correct directory (same as `models.py` unless specified):
    - `yolov3-face.cfg`
    - `yolov3-wider_16000.weights`  
  - Check for typos in filenames or paths in your code  
  - Ensure file permissions allow reading

- **Problem**: Out of memory during model loading  
  **Solution**:  
  - Close other memory-intensive applications  
  - Consider using a machine with more available RAM or try on a cloud instance

---

##  Connectivity Issues

- **Problem**: Application can't connect to Kafka  
  **Solution**:  
  - Confirm Kafka is running and healthy  
  - Check firewall or VPN settings that might block port `9092`  
  - Verify the Kafka broker address in your config matches the container/service name


# Kafka Core Concepts

## Kafka Architecture Overview

Kafka operates as a distributed messaging system that follows a client-server architecture. Applications connect to Kafka brokers via configuration settings:

```python
bootstrap_servers='localhost:9092'
```
**This setting establishes the fundamental connection between client applications and the Kafka cluster, serving as the entry point for all communications. The cluster maintains topics that organize message streams, while clients interact with these topics through well-defined APIs.**


The Kafka broker handles message persistence, replication, and delivery, functioning as an intermediary between producers and consumers while maintaining highly available service.

### Producer-Consumer Model

The implementation demonstrates Kafka's producer-consumer model through specialized components:

**Producers**
Producers are applications that publish messages to specific topics. The code shows multiple producer implementations:

- `A video frame producer that extracts and sends face detection data`
- `A media stream producer that publishes encoded audio and video chunks`
- `A messaging producer that sends chat data`
```python
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
producer.send(topic, result)
```

**Consumers**
Consumers subscribe to topics and process published messages. Different consumer implementations demonstrate varying consumption patterns:

- `A face data consumer that processes detection results and stores them in a database`
- `A video consumer that reconstructs frames from received data`
- `A threaded consumer within a web application that maintains an in-memory queue`

```python
consumer = KafkaConsumer(
    'Faces',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for msg in consumer:
    data = msg.value
    # Process the message
```
This decoupled architecture enables independent development, deployment, and scaling of producers and consumers.

## Topics and Partitions

This decoupled architecture enables independent development, deployment, and scaling of producers and consumers.

```python
# Different topics for different data domains
'Faces'        # Face detection data
'chat'         # Messaging data
'media-stream' # Video and audio streaming data
```
Topics are physically implemented as partitions, providing the foundation for parallelism and distributed processing. While partitioning configuration is not explicitly shown in the code, the Kafka client libraries manage the distribution of messages across partitions when multiple partitions exist.


Messages with the same key are guaranteed to be sent to the same partition, enabling ordering guarantees for related messages.

## Message Delivery Semantics

The implementation demonstrates various delivery semantics through configuration options:

```python
# Different offset reset strategies
auto_offset_reset='earliest'  # Process all available messages
auto_offset_reset='latest'    # Process only new messages
```

```python
# Ensuring message delivery
producer.flush()  # Blocks until messages are sent
```
```python
# Managing consumer offsets
enable_auto_commit=True  # Automatically track processed messages
```
These settings control the reliability guarantees:
- At-most-once: When producers don't wait for acknowledgments
- At-least-once: When producers confirm delivery and consumers track offsets
- Exactly-once: Requires additional configuration using transactions and idempotent producers

The implementation primarily uses at-least-once semantics, ensuring messages are never lost while accepting the possibility of duplicate processing.

## Getting Started
This section guides you through the practical steps to begin using Kafka in your application.

## Basic Setup

Before creating producers and consumers, you need to set up a basic Kafka environment:

```python
# Import the required libraries
from kafka import KafkaProducer, KafkaConsumer
import json

# Define broker connection information
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'example-topic'
```
Make sure your Kafka broker is running and accessible at the specified address before proceeding to the next steps.

## Simple Producer Example
The following example demonstrates how to create a basic producer that sends messages to a Kafka topic:

```python
# Create a Kafka producer with JSON serialization
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send a message to the topic
message = {"key": "value", "timestamp": "2023-04-09T12:00:00Z"}
producer.send(TOPIC_NAME, message)

# Ensure the message is sent before continuing
producer.flush()

print("Message sent successfully!")
```
This producer serializes Python dictionaries to JSON before sending them to the Kafka topic.

## Simple Consumer Example
Here's how to create a basic consumer that reads messages from a Kafka topic:

```python
# Create a Kafka consumer with JSON deserialization
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Process messages
print("Waiting for messages...")
for message in consumer:
    data = message.value
    print(f"Received: {data}")
    
    # Process the message data here
    
    # To exit the loop (in this example), break after processing one message
    break

consumer.close()
```
This consumer deserializes JSON messages back into Python dictionaries and processes them one by one.

## Configuration Options
Kafka clients offer numerous configuration options to customize behavior:

```python
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',                # Wait for all replicas to acknowledge
    retries=3,                 # Number of retries if the broker is unavailable
    batch_size=16384,          # Size of batches in bytes
    linger_ms=10,              # Delay in milliseconds to allow batching
    compression_type='gzip',   # Message compression type
    max_in_flight_requests_per_connection=1  # For strict ordering
)
```
**Consumer Configuration**
```python
consumer = KafkaConsumer(
    'example-topic',
    bootstrap_servers='localhost:9092',
    group_id='my-group',          # Consumer group ID
    auto_offset_reset='earliest',  # Start from beginning of topic
    enable_auto_commit=True,      # Automatically commit offsets
    auto_commit_interval_ms=5000, # Commit interval in milliseconds
    fetch_max_bytes=52428800,     # Max bytes to fetch per request
    max_poll_records=500,         # Max records per poll
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)
```
These configurations allow you to fine-tune performance, reliability, and behavior of your Kafka applications.

## API Reference
###  Producer API

**Module**: `producer.py`  
**Functionality**:
- Reads video frames using OpenCV.
- Applies YOLOv3-based face detection.
- Sends JSON results to the Kafka topic `Faces`.

**Kafka Configuration**:
```python
KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
```

Topic: Faces
Message Format:
```json
{
  "frame_id": 12,
  "total_faces": 3,
  "faces": [
    {
      "face_id": 0,
      "bounding_box": {"x": 100, "y": 120, "width": 50, "height": 50},
      "confidence": 0.89
    }
  ]
}

```

### Consumer API
**Module**: `consumer.py`  
Functionality:

- Subscribes to Kafka topic Faces.

- Deserializes JSON messages.

- Persists face data to MongoDB using insert_face_data().

```python
KafkaConsumer(
    'Faces',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)
```

MongoDB Integration:

- Assumes insert_face_data(data) in database.py.
---
##  Advanced Usage 

###  Serialization and Deserialization

- The **Producer** converts Python data (dictionary) to JSON before sending to Kafka.
- The **Consumer** reads the JSON from Kafka and turns it back into a Python dictionary.

```python
# Producer
value_serializer=lambda v: json.dumps(v).encode('utf-8')

# Consumer
value_deserializer=lambda v: json.loads(v.decode('utf-8'))
```

---

###  Error Handling and Retry Mechanism

- Right now, the app stops with `CTRL+C`.
- In the future, we try to implement:
  - **Retry logic**: Try sending or saving again if something fails.
  - **Logging errors**: Print or save errors to understand what went wrong.

---

###  Performance Tuning

- You can skip more frames by changing this line in `producer.py`:
  ```python
  frame_interval = int(fps / 3)
  ```
  Try `/2` or `/5` depending on how fast you want it.

- Use **batch writes** for MongoDB to save many face results at once.
- Kafka has settings like `linger.ms` and `batch.size` to send data faster and smarter.

---
##  Monitoring and Metrics

Monitoring helps ensure your system is working correctly, and lets you catch problems early. Below are suggestions to monitor the health and performance of your Kafka pipeline.

---

###  Kafka Monitoring

Use tools like:

- **Kafka Manager** or **Confluent Control Center** – to monitor:
  - Topic lag
  - Message throughput
  - Broker health
- **Prometheus + Grafana** (with JMX Exporter) – for real-time dashboards

**Metrics to track**:
- `Messages In/Out per second`
- `Under-replicated partitions`
- `Consumer group lag`
- `Producer retries/failures`

---

###  Producer Metrics

If you want to log metrics from the `producer.py`, consider:

- Logging each frame sent and face count:
  ```python
  print(f" Sent Frame {frame_id}: {result['total_faces']} faces")
  ```
Track dropped frames, retries, or exceptions using a logger.

For more advanced tracking:

- Use **prometheus_client** Python package to expose metrics from producer and consumer as HTTP endpoints.

### Consumer Metrics
**Monitor**:

- Number of messages consumed

- Insert success/failure count in MongoDB

To add basic timing:
```python
import time
start_time = time.time()
insert_face_data(data)
print(f"Insertion took {time.time() - start_time} seconds")
```
### MongoDB Monitoring
**MongoDB** Monitoring
Used  MongoDB Atlas or MongoDB Compass to:

- Track query times

- Monitor CPU/memory usage

- Review indexing effectiveness

  
# Deployment Guide

This guide provides step-by-step instructions to deploy the Kafka-based face detection system using Docker Compose.

---

## Production Best Practices

### Recommendations
- Use environment variables via `.env` for configuration.
- Separate dev/staging/prod Docker files if needed.
- Never commit actual secrets (e.g., passwords, keys) to version control.
- Use logging, retry, and error handling in producer/consumer scripts.
- Monitor Kafka, MongoDB, and Airflow health with dashboards or alerts.

---

### Scaling Considerations

### Techniques
- Use Kafka **partitions** to parallelize topic processing.
- Add more **consumers** in a **consumer group** to scale reads.
- Use multiple **Airflow Celery workers** for concurrent DAG execution.
- Enable **MongoDB sharding** for handling large volumes of face detection data.
- Control processing load using `frame_interval` in `producer.py`.

---

## Containerization with Docker

###  Services Overview

| Service       | Description                                 |
|---------------|---------------------------------------------|
| **Kafka**     | Message broker in KRaft mode                |
| **Kafka UI**  | Web interface for Kafka monitoring          |
| **RabbitMQ**  | Queue broker for Celery (Airflow)           |
| **PostgreSQL**| Database for Airflow metadata               |
| **Airflow**   | Task orchestration and scheduling platform  |
| **MongoDB**   | NoSQL DB for face detection results         |

###  How to Run
1. Create a `.env` file (with placeholders if sharing):
```env
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
RABBITMQ_DEFAULT_USER=admin
...
```

2. Start the stack:
```bash
docker compose up -d --build
```

3. Access services:
- Kafka UI: http://localhost:8080
- Airflow: http://localhost:8888
- RabbitMQ: http://localhost:15672

---

## Cloud Deployment Options

###  Recommended Services

| Component   | Cloud Alternative                       |
|-------------|------------------------------------------|
| Kafka       | Confluent Cloud, AWS MSK                 |
| MongoDB     | MongoDB Atlas                            |
| Container Hosting | GCP Cloud Run, AWS ECS, Azure Container Apps |
| Monitoring  | Grafana Cloud, Datadog, Prometheus Stack |

>  Pro Tip: Use managed cloud services to reduce infrastructure overhead.

---


# Examples

## Basic Examples

###  Running the System Locally

Start the producer and consumer from the command line:

```bash
python producer.py
python consumer.py
```

Sample output:
```bash
 Sent Frame 21: 3 faces
Received JSON:
{
  "frame_id": 21,
  "total_faces": 3,
  ...
}
```

---

## Real World Scenarios

###  Use Cases

- **Smart Surveillance**: Detect crowd levels in public areas using CCTV.
- **Retail Analytics**: Monitor foot traffic and customer behavior in stores.
- **Event Management**: Track audience density and movement during live events.
- **Campus Monitoring**: Integrate with security feeds to detect unusual gatherings.

---

## Integration with Other Systems

###  How to Extend

- **REST APIs**: Send results to analytics dashboards or visualization tools.
- **Database Sync**: Save face detection metadata to PostgreSQL for structured querying.
- **IoT Integration**: Trigger edge devices (alarms, cameras) based on crowd thresholds.
- **Cloud Logging**: Export structured logs to ELK stack or GCP Logging.

---

## Batch Processing

###  How It Works

- Use Airflow DAGs to:
  - Periodically scan folders for `.mp4` files
  - Trigger face detection
  - Store results in MongoDB or export as CSV

Example DAG task:
```python
run_producer = BashOperator(
    task_id='process_video',
    bash_command='python /opt/airflow/dags/producer.py'
)
```

---

## Stream Processing

###  Real-Time Analytics

- Connect the producer to a **live video source** (RTSP camera or webcam).
- Use Kafka to stream frames with minimal latency.
- Consumers process in near-real-time and store results in MongoDB.
- Combine with Airflow for post-processing pipelines or alerts.

---


## Contributing Guide

We welcome contributions to improve this Kafka-based face detection pipeline! Follow the guidelines below to ensure smooth collaboration.

---

#  Development Setup

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/sumituiet/kafka_python/
cd face-detection-kafka
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file using `.env.example` as a reference.

5. Run services:
```bash
docker compose up -d --build
```

---

##  Code Style Guidelines

- Follow **PEP8** for Python code.
- Use meaningful variable names and comments.
- Use `black` or `autopep8` for formatting:
```bash
black .
```

- Follow consistent naming and indentation conventions.

---

##  Testing

- Unit tests should go in the `tests/` folder.
- Use `pytest` to run tests:
```bash
pytest tests/
```

- Each function/module should have at least one test case.

---

##  Pull Request Process

1. Fork the repository.
2. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

3. Make your changes and commit them:
```bash
git commit -m "Add: brief description of change"
```

4. Push to your fork:
```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request:
   - Include a **clear title and description**
   - Mention any relevant issue numbers
   - Request review if needed

---

## Thank You

Thanks for helping improve the project! Your contributions make it better for everyone.


#  Troubleshooting Guide

This guide helps you resolve common issues and understand how to debug problems in the Kafka-based face detection system.

---

##  Common Issues

### 1. Kafka Producer not connecting
**Symptoms**: `NoBrokersAvailable` or connection timeout

**Solutions**:
- Ensure Kafka is running (`docker compose ps`)
- Check that you're using the correct port (usually `9092` or `29092`)
- Ensure environment variables in `.env` are correct

---

### 2. MongoDB insertion fails
**Symptoms**: `Connection refused` or no data appears in MongoDB

**Solutions**:
- Check that MongoDB is running (`docker ps`)
- Make sure `insert_face_data()` connects to the correct host and port
- Use `mongo` CLI or Compass to verify connection

---

### 3. YOLO model file errors
**Symptoms**: File not found errors for `yolov3-face.cfg` or `.weights`

**Solutions**:
- Ensure model files are placed in the correct working directory
- Use absolute paths or validate the relative path is correct

---

### 4. Airflow web UI is blank or errors
**Solutions**:
- Check Airflow logs using `docker compose logs airflow`
- Ensure `FERNET_KEY` is set and consistent across all services
- Run `airflow db upgrade` and restart services

---

##  Debugging Tips

- Use `print()` logs or structured logging (`logging`, `loguru`) in `producer.py` and `consumer.py`
- Enable Prometheus metrics and visualize with Grafana
- Use `docker logs <container>` to inspect container output
- Temporarily reduce `frame_interval` to speed up testing

---

##  FAQ

### Q: Can I run this without Docker?
**A**: Yes, but you'll need to install Kafka, MongoDB, and dependencies manually.

### Q: How do I connect to Kafka UI?
**A**: Visit `http://localhost:8080` (Kafka UI should be running via Docker).

### Q: What is the use of `frame_interval`?
**A**: It controls how frequently frames are processed. Higher values = fewer frames.

### Q: How do I add another consumer?
**A**: Clone `consumer.py`, give it a unique group ID, and run it in parallel.

### Q: How can I scale this in production?
**A**: Use Kafka partitions, deploy with Kubernetes, use MongoDB Atlas, and monitor with Prometheus.

---

#  Appendix

This section includes supporting materials such as definitions, external resources, and project version history.

---

##  Glossary

| Term          | Description |
|---------------|-------------|
| **Kafka**     | A distributed event streaming platform used to handle real-time data feeds. |
| **Producer**  | A service or program that publishes data to Kafka topics. |
| **Consumer**  | A service or program that subscribes to Kafka topics to read and process messages. |
| **YOLOv3**    | A real-time object detection algorithm used here for face detection. |
| **Airflow**   | A platform to programmatically author, schedule, and monitor workflows. |
| **MongoDB**   | A NoSQL database used for storing face detection results. |
| **Docker**    | A platform for developing and running applications inside containers. |

---

##  Additional Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [YOLOv3 Paper](https://pjreddie.com/media/files/papers/YOLOv3.pdf)
- [MongoDB Docs](https://www.mongodb.com/docs/)
- [Docker Docs](https://docs.docker.com/)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Prometheus Docs](https://prometheus.io/docs/introduction/overview/)

---

##  Version History

| Version | Date       | Description                    |
|---------|------------|--------------------------------|
| 1.0     | 2024-04-15 | Initial release with Kafka + YOLOv3 + MongoDB integration |
| 1.1     | 2024-04-18 | Docker Compose + Airflow integration |
| 1.2     | 2024-04-22 | Prometheus metrics and monitoring added |
| 1.3     | 2024-04-25 | Documentation and troubleshooting guide included |

---




















