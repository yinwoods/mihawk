import airflow
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python_operator import BranchPythonOperator

from mihawk.snippets.elastic import elastic_query


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['yinchengtao@4paradigm.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 4,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    dag_id='test_branch',
    default_args=args,
    schedule_interval='@daily'
)


def f_query_and_judge(dag, *args, **kwargs):
    params = kwargs['params']
    index = params['index']
    query_type = params['query_type']
    query_body = params['query_body']
    res = elastic_query(index, query_type, query_body)
    assert isinstance(res, dict)
    assert 'count' in res.keys()
    assert res['count'] > 100
    return 'send_mail'


query_and_judge = BranchPythonOperator(
    task_id='query',
    provide_context=True,
    python_callable=f_query_and_judge,
    params={
        'index': 'yijiupi_response',
        'query_type': 'count',
        'query_body': {
            'query': {
                'term': {'originalPlace': '海口'}
            }
        }
    },
    dag=dag
)


query_and_judge


if __name__ == '__main__':
    dag.cli()
