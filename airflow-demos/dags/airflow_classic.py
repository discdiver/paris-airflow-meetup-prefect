from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
import httpx
import pandas as pd

URL = "https://api.energidataservice.dk/dataset/PowerSystemRightNow"


def fetch_energy_production(start: str, end: str, **kwargs):
    """Fetch data from the API between start and end"""
    print(f"Fetching records from {start} until {end}")
    params = {
        "start": f"{start}T00:00",
        "end": f"{end}T00:00",
        "timezone": "utc"
    }
    resp = httpx.get(URL, params=params)
    resp.raise_for_status()
    records = resp.json().get("records", [])
    # Verify that we recieved all available records
    assert len(records) == resp.json().get("total", 0)

    kwargs["ti"].xcom_push("records", records)
    return records


def store_energy_production(path: str, **kwargs):
    """Persist as a parquet file to local disk or S3 via s3fs"""
    data = kwargs["ti"].xcom_pull(
        task_ids="fetch_energy_production",
        key="records"
    )

    print(f"Storing {len(data)} records at {path}")
    df = pd.DataFrame(data)
    df.to_parquet(path, index=False)


with DAG(
    "energy_production_classic",
    default_args={},
    description="Fetch and store energy production data",
    start_date=datetime(2022, 8, 1),
    schedule_interval="@daily",
    tags=["classic"]
) as dag:

    # The date range here is handled by Airflow macros
    start, end = "{{ ds }}", "{{ macros.ds_add(ds, 1) }}"
    path = f"./data/{start}_{end}.parquet"

    fetch_energy_production_task = PythonOperator(
        task_id='fetch_energy_production',
        python_callable=fetch_energy_production,
        op_args=(start, end,)
    )

    store_energy_production_task = PythonOperator(
        task_id='store_energy_production',
        python_callable=store_energy_production,
        op_args=(path,)
    )

    fetch_energy_production_task >> store_energy_production_task
