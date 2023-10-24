from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import clickhouse_connect

doc_md = """
#### Тестовое задание.
Автор: Ирина Бабинцева
"""

DEFAULT_ARGS = {
    'owner': 'babintseva',
    'provide_context': True
}

MSS_LIST = [262,460,310,208,510,404,250,724,234,311]

with DAG(
    dag_id='cell_towers_to_clickhouse',
    default_args=DEFAULT_ARGS,
    start_date=datetime(year=2023, month=9, day=4),
    schedule_interval='@once',
    tags=['cell_towers', 'babintseva'],
    max_active_runs=1,
    doc_md=doc_md
) as dag:

    start = DummyOperator(task_id='start')
    finish = DummyOperator(task_id='finish')

    def read_csv(file_name):
        for chunk in pd.read_csv(file_name, chunksize=10000):
            yield chunk


    def load_file_to_click():
        for df in read_csv(f'/tmp/cell_towers.csv'):
            load_to_clickhouse(df)


    def load_to_clickhouse(df: pd.DataFrame):
        client = clickhouse_connect.get_client(
            host='host.docker.internal',
            port=8123,
            user='',
            password='',
            verify=False
        )
        result_df = df[df['mcc'].isin(MSS_LIST)]
        client.insert_df('default.cell_towers', result_df)


    def deduplicate_data():
        client = clickhouse_connect.get_client(
            host='host.docker.internal',
            port=8123,
            user='',
            password='',
            verify=False
        )
        client.command(cmd='OPTIMIZE TABLE cell_towers FINAL DEDUPLICATE BY cell, net, area, mcc, radio, updated')


    download_file = BashOperator(
        task_id="download_file",
        bash_command="curl -o /tmp/cell_towers.csv.xz -L 'https://datasets.clickhouse.com/cell_towers.csv.xz' && xz -f -d /tmp/cell_towers.csv.xz",
        dag=dag,
    )

    load_file_to_clickhouse = PythonOperator(
        task_id="load_file_to_clickhouse",
        python_callable=load_file_to_click,
        dag=dag
    )

    deduplicate_table = PythonOperator(
        task_id="deduplicate_table",
        python_callable=deduplicate_data,
        dag=dag
    )


start >> download_file >> load_file_to_clickhouse >> deduplicate_table >> finish
