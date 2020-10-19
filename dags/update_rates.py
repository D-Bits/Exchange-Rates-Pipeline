from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, date
from requests import get
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 10, 1),
    "retries": 1,
}

dag = DAG("update_rates", schedule_interval="@daily", default_args=default_args)


def extract(**context):

    data = get(f"https://api.exchangeratesapi.io/history?start_at=2019-05-01&end_at={date.today()}&base=USD").json()
    # Create an XCOM for this task to be used in transform()
    context['ti'].xcom_push(key="data", value=data)


def transform(**context):

    # Fetch the JSON data from the above XCOM
    data = context["ti"].xcom_pull(key="data")
    # Load relevant JSON in DataFrame for processing
    df = pd.DataFrame(data)
