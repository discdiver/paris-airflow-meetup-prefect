from datetime import datetime, timedelta

from airflow.decorators import dag, task
import httpx
import pandas as pd

URL = "https://api.energidataservice.dk/dataset/PowerSystemRightNow"


@task
def fetch_energy_production(start: str, end: str) -> list:
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
    return records


@task
def store_energy_production(data: list, path: str):
    """Persist as a parquet file to local disk or S3 via s3fs"""
    print(f"Storing {len(data)} records at {path}")
    df = pd.DataFrame(data)
    df.to_parquet(path, index=False)


@dag(
    start_date=datetime(2022, 8, 1),
    schedule_interval="@daily",
    tags=["taskflow"]
)
def energy_production_taskflow():
    """Fetch and store energy production data"""
    # The date range here is handled by Airflow macros
    start, end = "{{ ds }}", "{{ macros.ds_add(ds, 1) }}"
    data = fetch_energy_production(start, end)
    path = f"./data/{start}_{end}.parquet"
    store_energy_production(data, path)
    

# The dag instance must be a top level key
energy_production_dag = energy_production_taskflow()
