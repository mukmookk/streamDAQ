from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from kafka_data_publisher import config_and_get_argparse, publish_to_kafka
from airflow.operators.sensors import ExternalTaskSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import timedelta, datetime
import calendar

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
    'schedule_interval': ['30 14-21 * * 1-5', '30 13-20 * * 1-5']
}

def conditionally_trigger(context, dag_run_obj):
    # DST는 3월 둘째 주 일요일에 시작하여 11월 첫째 주 일요일에 종료된다.
    start_dst = datetime(context['execution_date'].year, 3, 14 - ((5 + calendar.monthrange(context['execution_date'].year, 3)[0]) % 7))
    end_dst = datetime(context['execution_date'].year, 11, 7 - ((1 + calendar.monthrange(context['execution_date'].year, 11)[0]) % 7))

    if start_dst <= context['execution_date'] < end_dst:
        dag_run_obj.payload = {
            'message': 'summer_time_extraction_1'
        }
        return dag_run_obj
    else:
        dag_run_obj.payload = {
            'message': 'standard_time_extraction_1'
        }
        return dag_run_obj

with DAG('season_check',
         default_args=default_args,
         description='Check the current season',
         schedule_interval=None) as season_check_dag:

    trigger = TriggerDagRunOperator(
        task_id='trigger_dag',
        trigger_dag_id="{{ dag_run.payload['message'] }}",
        python_callable=conditionally_trigger,
        provide_context=True
    )

with DAG(
    'summer_time_extraction_1',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, summer time, first 30 minutes',
    schedule_interval="30-59 22 * * 2-6"
) as dag_summertime_extraction_1:

    @task
    def init_kafka_data_publisher():
        args = config_and_get_argparse()
        return args

    @task
    def publish_to_kafka_task(args):
        publish_to_kafka(args.ticker, args.topic, args.broker_ip, args.broker_port, args.mode)

    publish_to_kafka_task(init_kafka_data_publisher())

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

    init_kafka_data_publisher_2 = init_kafka_data_publisher()
    publish_to_kafka_task_2 = publish_to_kafka_task(init_kafka_data_publisher_2)

    wait_for_extraction >> publish_to_kafka_task_2

with DAG(
    'standard_time_extraction_1',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, standard time, first 30 minutes',
    schedule_interval="30-59 23 * * 1-5"
) as dag_standardtime_extraction_1:
    init_kafka_data_publisher_3 = init_kafka_data_publisher()
    publish_to_kafka_task(init_kafka_data_publisher_3)

with DAG(
    'standard_time_extraction_2',
    default_args=default_args,
    description='Data extraction and publishing to Kafka, standard time, after 30 minutes',
    schedule_interval="* 0-5 * * 2-6"
) as dag_standardtime_extraction_2:
    wait_for_extraction = ExternalTaskSensor(
        task_id='wait_for_extraction_1',
        external_dag_id='standard_time_extraction_1',
        external_task_id='publish_to_kafka_task',
        mode='reschedule',
    )

    init_kafka_data_publisher_4 = init_kafka_data_publisher()
    publish_to_kafka_task_4 = publish_to_kafka_task(init_kafka_data_publisher_4)

    wait_for_extraction >> publish_to_kafka_task_4