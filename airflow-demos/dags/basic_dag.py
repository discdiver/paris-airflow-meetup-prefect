from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def sub_1():
    """
    does a thing, also calls a different function
    """
    for i in range(3):
        sub_2()
    

def sub_2():
    """
    primary does a thing
    """
    print("I did it!")
    
    
def main():
    """
    Main dag function, calls sub_1
    """
    for i in range(4):
        sub_1()


with DAG(
    dag_id="example_dag",
    start_date=datetime(2023, 4, 1),
    schedule="@hourly",
    catchup=True
    ) as dag:
    
    task1 = PythonOperator(
        task_id="example_task4",
        python_callable=main)