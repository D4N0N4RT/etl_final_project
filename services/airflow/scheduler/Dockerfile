FROM apache/airflow:latest-python3.12

USER airflow
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/dags"

# Entrypoint
CMD ["scheduler"]