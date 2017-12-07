import arrow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from mihawk.snippets import dbapi
from mihawk.models.log_speed import LogSpeed
from mihawk.snippets.elastic import elastic_query
from mihawk.snippets.airflow import default_args


table = LogSpeed
log_name = 'ttgwm_user_action'
default_args.update({'email': 'yinchengtao@4paradigm.com'})


dag = DAG(
    dag_id=log_name+'_speed',
    default_args=default_args,
    schedule_interval='@daily'
)


def func(dag, *args, **kwargs):

    params = kwargs['params']
    index = params['index']
    query_type = params['query_type']
    query_body = params['query_body']
    response = elastic_query(index, query_type, query_body)

    log_speed = table(log_index=index,
                      time=arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                      params=params,
                      response=response)

    # 先保存当前count
    # 拿到最新的count
    # 用当前count与最新的count进行比较
    result = dbapi.latest_record(index, table)
    dbapi.commit(log_speed)
    latest_count = result.get('count')
    assert response.get('count') > latest_count


dsl = {
    'index': log_name,
    'query_type': 'count',
    'query_body': {}
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
