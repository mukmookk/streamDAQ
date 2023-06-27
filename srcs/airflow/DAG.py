from airflow import DAG
from airflow.decoraters import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from kafka_data_publisher import config_and_get_argparse, publish_to_kafka
from airflow.operators.sensors import ExternalTaskSensor
from datetime import timedelta

def get_postgres_conn(auto_commit=True):
    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    conn.autocommit = auto_commit
    return conn.cursor()

@task
def init_kafka_data_publisher():
    args = config_and_get_argparse()
    return args

@task
def publish_to_kafka(args):
    publish_to_kafka(args.ticker, args.topic, args.broker_ip, args.broker_port, args.mode)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'catchup': False,
    'tags': ['kafka', 'data_publisher'],
    'email': ['mukmookk@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': ['30 14-21 * * 1-5', '30 13-20 * * 1-5'] # 
}

with DAG(
    'summer_time_extraction_1',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, summer time, first 30 minutes',
    schedule_interval="30-59 22 * * 2-6"
) as dag_summertime_extraction_1:
    extraction_1_task = PythonOperator(
        task_id='publish_to_kafka_task',
        python_callable=publish_to_kafka,
        op_args=[init_kafka_data_publisher()]
    )

with DAG(
    'summer_time_extraction_2',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, summer time, after 30 minutes',
    schedule_interval="* 23,0-4 * * 2-6"
) as dag_summertime_extraction_2:
    wait_for_extraction = ExternalTaskSensor(
        task_id='wait_for_extraction_1',
        external_dag_id='summer_time_extraction_1',
        external_task_id='publish_to_kafka_task',
        mode='reschedule', 
    )

    extraction_2_task = PythonOperator(
        task_id='publish_to_kafka_task_2',
        python_callable=publish_to_kafka,
        op_args=[init_kafka_data_publisher()]
    )

    wait_for_extraction >> extraction_2_task

with DAG(
    'standard_time_extraction_1',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, standard time, first 30 minutes',
    schedule_interval="30-59 23 * * 1-5"
) as dag_standardtime_extraction_1:
    extraction_1_task = PythonOperator(
        task_id='publish_to_kafka_task_1',
        python_callable=publish_to_kafka,
        op_args=[init_kafka_data_publisher()]
    )

with DAG(
    'standard_time_extraction_2',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, standard time, after 30 minutes',
    schedule_interval="* 0-5 * * 2-6"
) as dag_standardtime_extraction_2:
    wait_for_extraction = ExternalTaskSensor(
        task_id='wait_for_extraction_1',
        external_dag_id='standard_time_extraction_1',
        external_task_id='publish_to_kafka_task_1',
        mode='reschedule',
    )

    extraction_2_task = PythonOperator(
        task_id='publish_to_kafka_task_2',
        python_callable=publish_to_kafka,
        op_args=[init_kafka_data_publisher()]
    )

    wait_for_extraction >> extraction_2_task