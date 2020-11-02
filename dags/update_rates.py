from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, date
from requests import get
from os import getenv
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 11, 1),
    "retries": 1,
}

# Run daily at 3pm, but skip weekends
dag = DAG("update_rates", schedule_interval="0 23 * * 1-5", default_args=default_args)


def extract(**context):

    data = get(f"https://api.exchangeratesapi.io/history?start_at=1999-01-01&end_at={date.today()}&base=USD").json()
    # Create an XCOM for this task to be used in transform()
    context['ti'].xcom_push(key="data", value=data)


def transform(**context):

    # Fetch the JSON data from the above XCOM
    data = context["ti"].xcom_pull(key="data")
    # Load relevant JSON in DataFrame for processing
    df = pd.DataFrame(
        data['rates']).transpose(
        ).reset_index(
        ).rename(columns={
            "index": "dates"
        }
    ).head(1).drop(['USD'], axis=1)

    context['ti'].xcom_push(key="df", value=df)


def load(**context):

    df = context["ti"].xcom_pull(key="df")
    db_conn = getenv("SQL_ALCHEMY_CONN")
    df.to_sql(
        'rates_history', 
        db_conn, 
        index=False, 
        method='multi', 
        if_exists='append',
    )


with dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract, provide_context=True)
    t2 = PythonOperator(task_id="transform", python_callable=transform, provide_context=True)
    t3 = PythonOperator(task_id="load", python_callable=load, provide_context=True)

    t1 >> t2 >> t3 
    