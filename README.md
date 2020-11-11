
# About 

Pipelines for updating a database of international exchange rates, using Apache Airflow.

## Running Locally

**Before anything else, you need Docker and `docker-compose` installed.*

- First, clone the repository to a directory of your choosing.
- Create a `.env.` file in the project directory, and add the following environment variables:
  - POSTGRES_USER=airflow
  - POSTGRES_PASSWORD=airflow
  - POSTGRES_DB=airflow
  - LOAD_EX=n
  - EXECUTOR=Local
  - SQL_ALCHEMY_CONN=(*postgres SQL Alchemy connection string*)
  - AIRFLOW__CORE__FERNET_KEY=(*fernet key for db connections*)
- Run, `docker-compose` up from the root of the project directory.

Once the services have all been bootstrap successfully, navigate to `localhost:8080/admin` in your browser to view the admin UI.

## DAG Guide 

- `seed_rates`: Run this to seed the db with data.