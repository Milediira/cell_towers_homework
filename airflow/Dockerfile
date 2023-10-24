FROM apache/airflow:2.6.3-python3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install clickhouse-connect
USER root
RUN apt-get update && apt-get install xz-utils