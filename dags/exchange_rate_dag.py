from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from google.cloud import bigquery

default_args = {
    'owner': 'rndrpp',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def fetch_and_load():
    # 1. Fetch from Frankfurter API
    url = "https://api.frankfurter.app/latest?to=JPY,SGD,IDR,USD"
    response = requests.get(url)
    data = response.json()

    # 2. Parse into a flat row
    row = {
        "fetched_at": datetime.utcnow().isoformat(),
        "base_currency": data["base"],
        "date": data["date"],
        "jpy": data["rates"]["JPY"],
        "sgd": data["rates"]["SGD"],
        "idr": data["rates"]["IDR"],
        "usd": data["rates"]["USD"],
    }

    # 3. Load into BigQuery
    client = bigquery.Client()
    table_id = "de-pipeline-demo-495506.exchange_rates.daily_rates"

    errors = client.insert_rows_json(table_id, [row])
    if errors:
        raise Exception(f"BigQuery insert error: {errors}")
    else:
        print(f"Row inserted: {row}")

with DAG(
    dag_id="exchange_rate_pipeline",
    default_args=default_args,
    description="Fetch exchange rates and load into BigQuery",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    fetch_and_load_task = PythonOperator(
        task_id="fetch_and_load",
        python_callable=fetch_and_load,
    )
