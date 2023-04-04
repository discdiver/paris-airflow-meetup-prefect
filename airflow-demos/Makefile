.PHONY: clean install start

export AIRFLOW_VERSION=2.3.3
export AIRFLOW_HOME=$(shell pwd)
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False

export PYTHON_VERSION=$(shell python --version | cut -d " " -f 2 | cut -d "." -f 1-2)
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

clean:
	rm -r \
		airflow.cfg \
		airflow.db \
		dags/__pycache__ \
		logs/ \
		standalone_admin_password.txt \
		webserver_config.py

install:
	pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
	pip install -r requirements.txt --constraint "${CONSTRAINT_URL}"

start:
	airflow standalone
