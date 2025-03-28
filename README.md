# Kafka python setup

this repository is the step-by-step guide to set up Kafka and create consumers and producers with a FastAPI example.

## Documentation

### Prerequisites
- Python 3.10 or higher
- Kafka server docker running 
- uv 0.6 or higher
- FastAPI framework installed
- docker

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/sumituiet/kafka_python.git
2. Setup the kafka server and other services:
```bash
docker-compose up -d
```
3. setup virtual environment 
```bash 
uv venv
```
4. Install dependencies:
    ```bash
    uv install
    ```

### Usage
1. Start the Kafka server and ensure it is running.
2. Set up the environment using `uv`:
    ```bash
    fastapi dev app.py
    ```
3. Access the API documentation at `http://127.0.0.1:8000/docs`.

### Features
- Kafka producer and consumer implementation.
- FastAPI integration for API endpoints.
- Example use cases for message publishing and consumption.

### Project Structure
- `app/`: Contains the FastAPI application code.
- `kafka/`: Includes Kafka producer and consumer logic.
- `pyproject.toml`: Lists the Python dependencies.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.