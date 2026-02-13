"""
E-commerce Pipeline DAG
Orkestrira: Data Generation -> Parquet -> GCS -> BigQuery -> dbt
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "dorian",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def generate_and_export_data():
    """Generira podatke i sprema u Parquet"""
    import sys
    sys.path.insert(0, "/opt/airflow/src/ingestion")

    from generator import generate_all_data
    from exporter import export_to_parquet

    print("[Airflow] Generiram podatke...")
    data = generate_all_data(num_customers=100, num_products=50, num_orders=200)

    print("[Airflow] Spremam u Parquet...")
    export_to_parquet(data, "/opt/airflow/data/raw")
    print("[Airflow] Podaci generirani i spremljeni!")


def upload_to_gcs():
    """Uploada Parquet datoteke na GCS"""
    import sys
    sys.path.insert(0, "/opt/airflow/src/ingestion")

    from gcs_uploader import upload_all_parquet_files

    print("[Airflow] Uploadam na GCS...")
    upload_all_parquet_files(
        credentials_path="/opt/airflow/credentials.json",
        bucket_name="ecommerc-raw-dorian",
        data_dir="/opt/airflow/data/raw"
    )
    print("[Airflow] Upload završen!")


def load_to_bigquery():
    """Učitava podatke iz Parquet u BigQuery"""
    import sys
    sys.path.insert(0, "/opt/airflow/src/ingestion")

    from bigquery_loader import load_all_tables

    print("[Airflow] Učitavam u BigQuery...")
    load_all_tables(
        credentials_path="/opt/airflow/credentials.json",
        data_dir="/opt/airflow/data/raw",
        dataset_id="ecommerce_raw"
    )
    print("[Airflow] BigQuery učitavanje završeno!")


with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    description="E-commerce pipeline: Generate -> Parquet -> GCS -> BigQuery -> dbt",
    schedule_interval="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ecommerce", "pipeline"],
) as dag:

    generate_task = PythonOperator(
        task_id="generate_and_export",
        python_callable=generate_and_export_data,
    )

    gcs_task = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
    )

    bigquery_task = PythonOperator(
        task_id="load_to_bigquery",
        python_callable=load_to_bigquery,
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt/ecommerce && dbt run --profiles-dir /opt/airflow/dbt",
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt/ecommerce && dbt test --profiles-dir /opt/airflow/dbt",
    )

    generate_task >> gcs_task >> bigquery_task >> dbt_run_task >> dbt_test_task
