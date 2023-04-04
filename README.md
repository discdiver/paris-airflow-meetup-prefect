# Airflow Paris 

This repo contains code shown in the Paris Apache Airflow Meetup from April 4, 2023.

The [Prefect demos folder](./prefect-demos) contains examples of getting started with Prefect and using it for concurrent and parallel workflows.

The [Marvin demos folder](./marvin-demos/) contains examles of using Marvin's AI Functions to generate outputs with LLMs. 

The [Airflow demos folder](./airflow-demo/) contains some small pipelines in Airflow with and without Prefect for observability. There are a few versions of the same pipeline. The final version shows Prefect without airflow.

1. [original.py](./airflow-demos/dags/original.py) shows the pipeline without any orchestration
2. [airflow_classic.py](/airflow-demos/dags/airflow_classic.py) shows the pipeline as a classic airflow DAG
3. [airflow_taskflow.py](./airflow-demos/dags/airflow_taskflow.py) shows the pipeline as a [TaskFlow](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html) airflow DAG
4. [airflow_taskflow_with_prefect_flow.py](./airflow-demos/dags/airflow_taskflow_with_prefect_flow.py) shows the Airflow DAG AND a Prefect flow.
5. [prefectified.py](./airflow-demos/dags/prefectified.py) shows the pipeline as a standalone Prefect flow.

There are also examples showing how to make an Airflow DAG into an observable event.
1. [basic_dag.py](./airflow-demos/dags/basic_dag.py)
2. [basic_dag_with_prefect_event.py]((./airflow-demos/dags/basic_dag_with_prefect_event.py)

## Getting Started for Prefect

Install Prefect with `pip install -U prefect` in a Python virtual environment.

Create a [Prefect Cloud account](https://app.prefect.cloud).

Authenticate your terminal to Prefect Cloud with `prefect cloud login`.

## Getting Started for Marvin

Install Marvin wiht `pip install -U marvin` in a Python 3.9+ virtual environment.

Run `marvin chat` in the terminal. 

Provide your OpenAPI API key when prompted. Get an API key at openai.com if needed.

## Getting Started for Airflow

Create a new Python virtual environment and install the dependencies with

```sh
make install
```

Now you can start a local instance of airflow,

```sh
make start
```

Open up [http://0.0.0.0:8080](http://0.0.0.0:8080) in your browser to access the UI.

## Architecture

The component services of airflow can be understood by looking at the official [docker-compose.yaml](https://github.com/apache/airflow/blob/main/docs/apache-airflow/start/docker-compose.yaml). In a minimal setup you have,

* a **database** for metadata which is sqlite by default but typically postgres
* a **webserver** that serves the UI
* a **scheduler** that runs tasks using an **executor** which is typically `LocalExecutor` for local execution and `CeleryExecutor` for distributed execution

In a more scalable setup using Celery you would add,

* one or more **workers** that executes tasks
* a **redis** instance to broker between scheduler and workers
* optionally a **flower** UI for monitoring Celery

Airflow also has extensive support for Kubernetes, including an [official Helm chart](https://airflow.apache.org/docs/helm-chart/stable/index.html).

![](https://airflow.apache.org/docs/apache-airflow/stable/_images/arch-diag-basic.png)
