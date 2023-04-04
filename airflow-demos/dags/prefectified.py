from datetime import datetime, timedelta

import httpx
import pandas as pd
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash

URL = "https://api.energidataservice.dk/dataset/PowerSystemRightNow"


@task(retries=3, retry_delay_seconds=5, cache_key_fn=task_input_hash)
def fetch_energy_production(start: datetime, end: datetime):
    """Fetch data from the API between start and end"""
    get_run_logger().info(f"Fetching records from {start} until {end}")
    date_format = "%Y-%m-%dT00:00"
    params = {
        "start": start.strftime(date_format),
        "end": end.strftime(date_format),
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
    get_run_logger().info(f"Storing {len(data)} records at {path}")
    df = pd.DataFrame(data)
    df.to_parquet(path, index=False)


@flow
def backfill(
    since: datetime = (datetime.now() - timedelta(days=20)),
    until: datetime = datetime.now()
):
    """Fetch and store energy production data between the given dates"""
    period = [(since + timedelta(days=i)).date() for i in range(0, (until - since).days)]
    for day in period:
        start, end = day, day + timedelta(days=1)
        data = fetch_energy_production.submit(start, end)
        path = f"./data/{start.strftime('%Y-%m-%d')}_{end.strftime('%Y-%m-%d')}.parquet"
        store_energy_production.submit(data, path)

if __name__ == "__main__":
    backfill()
