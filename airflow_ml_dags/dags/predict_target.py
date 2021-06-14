import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "email": ["stponfilenko@gmail.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# !!! HOST folder(NOT IN CONTAINER) replace with yours !!!
HOST_DATA_DIR = '/home/stacy/Work/made/prod2/creative-crisis/airflow_ml_dags/'

with DAG(
        "predict_target",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}/data:/data"]
    )

    predict = DockerOperator(
        image="airflow-predict",
        command="--input-dir /data/processed/{{ ds }} "
                "--model-dir /data/model/{{ var.value.model }} "
                "--output-dir /data/predictions/{{ ds }}",
        task_id="docker-airflow-predict",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}/data:/data"]
    )

    preprocess >> predict
