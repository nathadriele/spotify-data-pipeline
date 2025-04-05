from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'nathadriele',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
    'depends_on_past': False,
    'email_on_failure': False,
}

with DAG(
    dag_id='spotify_data_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    description='ETL pipeline: Extract recent tracks from Spotify, transform with dbt and validate with dbt tests',
    tags=['spotify', 'etl', 'dbt'],
) as dag:

    extract_recent_tracks = BashOperator(
        task_id='extract_recent_tracks',
        bash_command='python /opt/airflow/src/save_recent_tracks.py',
    )

    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt/spotify && dbt run',
    )

    run_dbt_tests = BashOperator(
        task_id='run_dbt_tests',
        bash_command='cd /opt/airflow/dbt/spotify && dbt test',
    )

    extract_recent_tracks >> run_dbt_models >> run_dbt_tests
