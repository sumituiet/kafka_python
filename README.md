### 🏗️ Architecture

The system is designed to handle image ingestion and processing via Kafka, trigger Airflow workflows, and return results asynchronously.

#### 🔄 Flow Overview

1. **Client** uploads an image via FastAPI.
  
2. **FastAPI** compresses and sends the image to a **Kafka topic**.
  
3. An **Airflow DAG** is triggered via REST API.
  
4. Downstream workers or sensors consume Kafka messages for processing.
  
5. Once processing is complete, results are published to a **Kafka result topic**.
  
6. **FastAPI** listens to the result topic and returns the final output to the client.
  

#### 🖼️ Architecture Diagram

```
+---------+        HTTP         +-----------+       Kafka        +------------+
|  Client |  ---------------->  |  FastAPI  |  ----------------> |   Kafka    |
+---------+   POST /upload/     +-----------+   Image Topic     +------------+
                                                      |
                                                      v
                                               +-------------+
                                               | Airflow DAG |
                                               | (Triggered) |
                                               +-------------+
                                                      |
                                            Kafka Result Topic
                                                      |
                                                      v
                                              +--------------+
                                              |   FastAPI    |
                                              | KafkaConsumer|
                                              +--------------+
                                                      |
                                                      v
                                                JSON Result
```

#### 🔧 Components

| Component | Role |
| --- | --- |
| **FastAPI** | API server to handle file uploads and interact with Kafka and Airflow |
| **Kafka** | Message queue used for ingesting image blobs and returning results |
| **Airflow** | Workflow orchestrator that handles image processing logic |
| **Docker Compose** | Used to run Kafka, Zookeeper, and other services locally |

> This modular design ensures decoupling of services and easy scaling of Kafka consumers and DAG workers.

### 🖥️Backend setup

> For more details, please refer to the official [Kafka documentation](https://kafka.apache.org/documentation/).

### ✅ Prerequisites

- Python 3.10 or higher
  
- Kafka server running via Docker
  
- [`uv`](https://github.com/astral-sh/uv) 0.6 or higher
  
- FastAPI framework installed
  
- Docker and Docker Compose
  

---

### 🔧 Installation

1. **Clone the repository:**
  
  ```bash
  git clone https://github.com/sumituiet/kafka_python.git
  cd kafka_python
  ```
  
2. **Set up Kafka server and services:**
  
  ```bash
  docker-compose up -d
  ```
  
3. **Set up virtual environment using `uv`:**
  
  ```bash
  uv venv
  ```
  
4. **Install Python dependencies:**
  
  ```bash
  uv install
  ```
  

---

### 🚀 Usage

1. Ensure Kafka is running via Docker.
  
2. Run the FastAPI app using `uv`:
  
  ```bash
  fastapi dev app.py
  ```
  
3. Access the interactive API docs:
  
  - Swagger UI: http://127.0.0.1:8000/docs
    
  - ReDoc: http://127.0.0.1:8000/redoc
    

---

### 💡 Features

- Kafka producer and consumer setup using `kafka-python`.
  
- FastAPI integration for API endpoints.
  
- Example use cases for real-time image processing and Airflow orchestration.
  
- Airflow DAG triggering and Kafka-based messaging.
  

---

### 📁 Project Structure

```
kafka_python/
│
├── app/                   # FastAPI app code
│   └── app.py             # Main API endpoints and Kafka logic
│
├── kafka/                 # Kafka producer/consumer utilities
│   ├── producer.py
│   └── consumer.py
│
├── docker-compose.yml     # Kafka, Zookeeper, and dependencies
├── pyproject.toml         # Project dependencies
└── README.md              # Project documentation
```

---

### 🔗 API Endpoints Summary

#### `POST /upload/`

- Uploads an image, compresses it, sends to Kafka, triggers an Airflow DAG, and returns Kafka result.
  
- Params:
  
  - `file`: JPEG/PNG image
    
  - `dag_id`: Airflow DAG ID (optional, default: `object_detection_single_task`)
    

#### `POST /trigger-test-kafka-dag/`

- Triggers the `test_kafka_in_virtualenv_dag` in Airflow and listens for a message on Kafka topic `kafka_test`.
