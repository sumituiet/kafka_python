# Apache Airflow Integration

### This project uses Apache Airflow to orchestrate Kafka message production and consumption workflows.
* * *
All Airflow-related files are located in the `airflow/dags/` directory:

`kafka_producer_dag.py`: Defines a DAG that produces messages to a Kafka topic.

`kafka_consumer_dag.py`: Defines a DAG that consumes messages from a Kafka topic.
* * *
##  Requirements
Make sure the following dependencies are installed:
```bash
pip install apache-airflow apache-airflow-providers-apache-kafka
```
* * *
## Kafka Connection Setup
Before running the DAGs, configure a Kafka connection in Airflow:

1. Go to the Airflow UI (http://localhost:8080)

2. Navigate to Admin → Connections

3. Click on + Add a new record.

4. Add a new connection:

	- Conn Id: `kafka_default`
	
	- Conn Type: `Kafka`

```jason
{
  "bootstrap.servers": "localhost:9092"
}
```
* * *
## How the DAGs Work
`kafka_producer_dag.py`
- Uses a Python function to produce test messages to the Kafka topic `test_topic`.
- Scheduled to run every minute (adjustable via `schedule_interval`).

`kafka_consumer_dag.py`
- Consumes messages from the same topic `test_topic`.
- Processes the messages and logs the output.

* * *
## Running Airflow
To start Airflow services:

```bash
airflow db init
airflow webserver -p 8080
airflow scheduler
```
* * *
## Testing the Setup
To test the Kafka-Airlow integration:
1. Trigger the `kafka_producer_dag` from the Airflow UI.
2. Ensure that messages are produced to the `test_topic`.
3. Trigger the `kafka_consumer_dag` to consume messages from the same topic.
4. Verify that the consumer function processes the messages as expected
   
* * *
## Custom Functions
The DAGs utilize custom Python functions for producing and consuming messages:

- Producer Function: Generates messages to be sent to Kafka.

- Consumer Function: Processes messages received from Kafka.

These functions are defined within the DAG files and are referenced by the respective operators
* * *
## Monitoring and Logs
Airflow provides a comprehensive UI to monitor DAG runs and task logs:
1. Access the Airflow UI at `http://localhost:8080`.

2. Select the desired DAG (`kafka_producer_dag` or `kafka_consumer_dag`).

3. View the DAG's execution status, task instances, and logs for debugging and monitoring purposes.

* * *