import logging
import os
from datetime import datetime
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

collection_name = 'product_price_history'

logging.basicConfig(level=logging.INFO)


def extract(**kwargs):
    mongo_hook = MongoHook(mongo_conn_id='mongo_conn')
    client = mongo_hook.get_conn()
    db_name = os.getenv("MONGO_DB", "source_db")
    collection = client[db_name][collection_name]

    extracted_data = list(collection.find({}, {"_id": 0}))
    logging.info(f"Found {len(extracted_data)} documents")

    kwargs['ti'].xcom_push(key='extracted_data', value=extracted_data)


def transform(**kwargs):
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract', key='extracted_data')

    if not extracted_data:
        return

    df = pd.DataFrame(extracted_data)

    df_exploded = df.explode("price_changes").reset_index(drop=True)

    price_history_df = df_exploded["price_changes"].apply(pd.Series)

    df_transformed = pd.concat([df_exploded.drop(columns=["price_changes"]), price_history_df], axis=1)

    df_transformed.drop_duplicates(subset=["session_id"], inplace=True)
    df_transformed.fillna("", inplace=True)

    ti.xcom_push(key='transformed_data', value=df_transformed.to_dict(orient='records'))


def load(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform', key='transformed_data')

    if not transformed_data:
        return

    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    engine = pg_hook.get_sqlalchemy_engine()

    df = pd.DataFrame(transformed_data)

    df['date'] = pd.to_datetime(df['date'])

    neworder = ['product_id', 'date', 'price', 'currency', 'current_price']
    df = df.reindex(columns=neworder)

    df.set_index(['product_id', 'date'], inplace=True)

    df.to_sql(collection_name, con=engine, if_exists="replace", index=True)

    logging.info(f"Inserted {len(df)} rows")


with DAG(
    dag_id="product_price_history_etl_replication",
    start_date=datetime(2025, 3, 17),
    catchup=False,
    tags=["replication"],
) as dag:
    task_start = EmptyOperator(task_id='start', dag=dag)
    task_finish = EmptyOperator(task_id='finish', dag=dag)

    task_extract = PythonOperator(task_id='extract', python_callable=extract, provide_context=True, dag=dag)
    task_transform = PythonOperator(task_id='transform', python_callable=transform, provide_context=True, dag=dag)
    task_load = PythonOperator(task_id='load', python_callable=load, provide_context=True, dag=dag)

    task_start >> task_extract >> task_transform >> task_load >> task_finish
