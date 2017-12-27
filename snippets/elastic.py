import json
from mihawk.snippets.config import elastic_config
from elasticsearch import Elasticsearch


elastic_client = Elasticsearch(json.loads(elastic_config['host']), timeout=30)


def elastic_query(index, query_type, query_body):
    if query_type == 'count':
        return elastic_client.count(index=index, body=query_body)
    elif query_type == 'search':
        return elastic_client.search(index=index, body=query_body)
    elif query_type == 'mapping':
        return elastic_client.indices.get(index)
