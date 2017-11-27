# 查询yijiupi_response日志中白酒的个数
import airflow
from airflow.models import DAG
from airflow.operators import PythonOperator
from airflow.operators.dummy_operator import DummyOperator


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}


dag = DAG(
    dag_id='test',
    default_args=args,
    schedule_interval='1 * * * *'
)


def test():
    assert False


branching = PythonOperator(
    task_id='branching',
    python_callable=test,
    dag=dag
)

dummy = DummyOperator(
    task_id='dummy',
    dag=dag
)

branching >> dummy


if __name__ == '__main__':
    dag.cli()
