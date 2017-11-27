import json
from mihawk.snippets.common import elastic_config
from elasticsearch import Elasticsearch


es_client = Elasticsearch(json.loads(elastic_config['host']), timeout=30)


def elastic_query(index, query_type, query_body):
    if query_type == 'count':
        return es_client.count(index=index, body=query_body)
    elif query_type == 'search':
        return es_client.search(index=index, body=query_body)
