from prefect import flow, task
from prefect_dask import DaskTaskRunner

@task
def task1(x: int) -> int:
    return x + 10

@task
def task2(x: int) -> int:
    return -x

@flow(task_runner=DaskTaskRunner)
def run_my_flow_parallel(n: int):
    task2.map(task1.map(range(n)))

if __name__ == "__main__":
    n = 1000
    run_my_flow_parallel(n)
