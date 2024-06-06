from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'provide_context': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dbt_backfill',
    default_args=default_args,
    description='A DAG to backfill dbt models',
    schedule_interval=None,  # assuming a manual trigger
)


def set_backfill_dates(**kwargs):
    start_date = kwargs['dag_run'].conf.get('start_date')
    end_date = kwargs['dag_run'].conf.get('end_date')
    return (
        f"dbt run --models hourly_sorting_aggregates "
        f"--profiles-dir /path/to/profiles "
        f"--project-dir /path/to/project "
        f"--vars '{{{{ start_date: \"{start_date}\", end_date: \"{end_date}\" }}}}'"
    )


set_dates = PythonOperator(
    task_id='set_backfill_dates',
    python_callable=set_backfill_dates,
    provide_context=True,
    dag=dag,
)

dbt_run_backfill = BashOperator(
    task_id='dbt_run_backfill',
    bash_command="{{ task_instance.xcom_pull(task_ids='set_backfill_dates') }}",
    dag=dag,
)

dbt_run_downstream_backfill = BashOperator(
    task_id='dbt_run_downstream_backfill',
    bash_command=(
        "dbt run "
        "--models downstream_table "
        "--profiles-dir /path/to/profiles "
        "--project-dir /path/to/project"
    ),
    dag=dag,
)

# define task order
set_dates >> dbt_run_backfill >> dbt_run_downstream_backfill
