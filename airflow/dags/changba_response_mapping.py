import arrow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from mihawk.snippets import dbapi
from mihawk.models.logs import Logs
from mihawk.snippets.elastic import elastic_query
from mihawk.snippets.airflow import default_args


default_args.update({'email': 'yinchengtao@4paradigm.com'})


dag = DAG(
    dag_id='changba_response_mapping',
    default_args=default_args,
    schedule_interval='@hourly'
)


def func(dag, *args, **kwargs):

    params = kwargs['params']
    index = params['index']
    query_type = params['query_type']
    query_body = params['query_body']
    mapping = query_body['mapping']

    response = elastic_query(index, query_type, query_body)
    properties = response[index]['mappings'][index]['properties']

    logs = Logs(log_index=index,
                time=arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                params=params,
                response=response)
    dbapi.commit(logs)

    for key, value in mapping.items():
        assert key in properties.keys()
        assert value['type'] == properties[key]['type']
    return response


dsl = {
    'index': 'changba_response',
    'query_type': 'mapping',
    'query_body': {
        'mapping': {
            'responseTime': {'type': 'long'},
            'responseTimeStd': {'type': 'date'},
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
