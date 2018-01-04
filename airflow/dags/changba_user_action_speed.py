import arrow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from mihawk.common import dbapi
from mihawk.models.mihawk import LogSpeed
from mihawk.common.elastic import elastic_query
from mihawk.common.airflow import default_args


table = LogSpeed
log_name = 'changba_user_action'
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
    record_count = response.get('count', 0)

    log_speed = table(log_index=index,
                      time=arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                      params=params,
                      response=response,
                      record_count=record_count)

    # 先保存当前count
    # 拿到最新的count
    # 用当前count与最新的count进行比较
    result = dbapi.latest_record(index, table)
    dbapi.commit(log_speed)
    last_record_count = result.get('count')
    assert record_count > last_record_count


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
