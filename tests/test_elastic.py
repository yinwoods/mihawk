from mihawk.snippets.elastic import elastic_query


def test_elastic_query_count():
    res = elastic_query('yijiupi_response', query_type='count', query_body={
        "query": {
            "term": {"originalPlace": "厦门"}
        }
    })
    assert isinstance(res, dict)
    assert 'count' in res.keys()
    assert res['count'] > 0


def test_elastic_query_search():
    res = elastic_query('yijiupi_response', query_type='search', query_body={
        "query": {
            "term": {"originalPlace": "海口"}
        }
    })
    assert 'hits' in res.keys()
    assert 'total' in res['hits'].keys()
    assert res['hits']['total'] > 0


if __name__ == '__main__':
    # test_elastic_query_count()
    test_elastic_query_search()
