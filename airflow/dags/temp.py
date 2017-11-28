from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from mihawk.snippets.elastic import elastic_query
from mihawk.snippets.airflow import default_args


default_args.update({'email': 'yinchengtao@4paradigm.com'})

dag = DAG(
    dag_id='yijiupi_original_place_haikou',
    default_args=default_args,
    schedule_interval='@hourly'
)


def func(dag, *args, **kwargs):
    params = kwargs['params']
    index = params['index']
    query_type = params['query_type']
    query_body = params['query_body']
    res = elastic_query(index, query_type, query_body)
    assert isinstance(res, dict)
    assert 'count' in res.keys()
    assert res['count'] > 2000
    return res


dsl = {
    'index': 'yijiupi_response',
    'query_type': 'count',
    'query_body': {
        'query': {
            'term': {'originalPlace': '海口'}
        }
    }
}


query = PythonOperator(
    task_id='query',
    provide_context=True,
    python_callable=func,
    params=dsl,
    dag=dag
)


dummy = DummyOperator(
    task_id='dummy',
    dag=dag
)


query >> dummy


if __name__ == '__main__':
    dag.cli()
