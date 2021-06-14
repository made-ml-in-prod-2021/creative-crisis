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
        "train_model",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=days_ago(5),
) as dag:

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}/data:/data"]
    )

    split = DockerOperator(
        image="airflow-split",
        command="--input-dir /data/processed/{{ ds }} --output-dir /data/processed/{{ ds }} --val-size 0.25",
        task_id="docker-airflow-split",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}/data:/data"]
    )

    train = DockerOperator(
        image="airflow-train",
        command="--input-dir /data/processed/{{ ds }} --output_model-dir /data/model/{{ ds }}",
        task_id="docker-airflow-train",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}/data:/data"]
    )

    validate = DockerOperator(
        image="airflow-validate",
        command="--input-dir /data/processed/{{ ds }} --model-dir /data/model/{{ ds }}",
        # command="--input-dir /data/processed/{{ ds }} --model-  --output-dir /data/predicted/{{ ds }}",
        task_id="docker-airflow-validate",
        do_xcom_push=False,
        volumes=[f"{HOST_DATA_DIR}/data:/data", f"{HOST_DATA_DIR}/logs:/logs"]
    )

    preprocess >> split >> train >> validate
