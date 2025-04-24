from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import time

# Define a simple Python function to be used in the tasks
def print_hello():
    print("Hello, Airflow!")

def wait_for_a_while():
    print("Waiting for 5 seconds...")
    time.sleep(5)
    print("Done waiting!")

# Define the DAG
default_args = {
    'start_date': datetime(2024, 4, 20),  # Ensure this date is in the past for testing
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple test DAG to print and wait',
    catchup=True,
    tags=['example']
)

# Define the tasks
task1 = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

task2 = PythonOperator(
    task_id='wait_for_a_while',
    python_callable=wait_for_a_while,
    dag=dag,
)

# Set task dependencies
task1 >> task2  # task2 will run after task1 finishes
