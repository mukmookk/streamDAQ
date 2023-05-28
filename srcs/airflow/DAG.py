from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['mukmookk@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kafka_data_publisher',
    default_args=default_args,
    description='run kafka_data_publisher.py',
    schedule_interval="0 22-23,0-3 * * *")

t1 = BashOperator(
    task_id='run_python_script',
    bash_command='python /opt/streamdaq/srcs/data_pipeline/kafka/kafka_data_publisher.py',
    dag=dag,
)