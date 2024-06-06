from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'dbt_regular_processing',
    default_args=default_args,
    description='A DAG to run dbt models for regular processing',
    schedule_interval='@daily',
)

dbt_run_agg = BashOperator(
    task_id='dbt_run_agg',
    bash_command='dbt run --models agg_table --profiles-dir /path/to/profiles --project-dir /path/to/project',
    dag=dag,
)

dbt_run_downstream = BashOperator(
    task_id='dbt_run_downstream',
    bash_command='dbt run --models downstream_table --profiles-dir /path/to/profiles --project-dir /path/to/project',
    dag=dag,
)

# define task order
dbt_run_agg >> dbt_run_downstream
