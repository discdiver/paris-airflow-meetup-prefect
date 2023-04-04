from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from prefect.events import emit_event

def sub_1():
    """does a thing, also calls a different function"""
    for i in range(3): sub_2()

def sub_2():
    """does another thing"""
    pass

def main():
    """Main dag function, calls sub1"""
    emit_event(event="airflow.dag.started", resource={"prefect.resource.id": "airflow.dag.task.main"})
    for i in range(4): sub_1()
    emit_event(event="airflow.dag.finished", resource={"prefect.resource.id": "airflow.dag.task.main"})

with DAG(
    dag_id="example_dag_prefect_observe",
    start_date=datetime(2023, 4, 1),
    schedule="@hourly",
    catchup=False
    ) as dag:
    
    task1 = PythonOperator(
        task_id="example_task",
        python_callable=main)