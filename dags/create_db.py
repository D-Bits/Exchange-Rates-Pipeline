from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 11, 1),
    "retries": 1,
}

dag = DAG("create_db", schedule_interval=None, template_searchpath=['/usr/local/airflow/dags/sql'], catchup=False, default_args=default_args)


with dag:

    t1 = PostgresOperator(task_id="create_db", sql="CREATE DATABASE rates;", postgres_conn_id='postgres_main', autocommit=True)
    t2 = PostgresOperator(task_id="create_tables", sql="tables.sql", database="rates", postgres_conn_id='postgres_main', autocommit=True)

    t1 >> t2
