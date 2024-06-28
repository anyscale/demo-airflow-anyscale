from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from anyscale_provider.operators.anyscale import SubmitAnyscaleJob


# Define the Anyscale connection
ANYSCALE_CONN_ID = "anyscale_conn"

# Constants
FOLDER_PATH = Path(__file__).parent / "ray_scripts"

dag = DAG(
    "sample_anyscale_job_workflow",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2024, 4, 2),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A DAG to interact with Anyscale triggered manually",
    schedule=None,  # This DAG is not scheduled, only triggered manually
    catchup=False,
)

submit_anyscale_job = SubmitAnyscaleJob(
    task_id="submit_anyscale_job",
    conn_id=ANYSCALE_CONN_ID,
    name="Simple Anyscale Job",
    working_dir=str(FOLDER_PATH),
    entrypoint="python ray_job.py",
    max_retries=1,
    job_timeout_seconds=3000,
    poll_interval=10,
    dag=dag,
)


# Defining the task sequence
submit_anyscale_job
