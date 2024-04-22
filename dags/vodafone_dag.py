from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from scraper.airpods import vodafone_etl
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    "vodafone_etl",
    default_args=default_args,
    description='vodafone etl dag',
    schedule='0 */6 * * *',
    start_date=datetime(2024, 4, 19),
    catchup=False,
    tags=['store', 'products'],
) as dag:
    insert_info = PythonOperator(
        task_id='insert_info',
        python_callable=vodafone_etl,
    )


