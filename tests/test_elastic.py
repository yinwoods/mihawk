from mihawk.common.elastic import elastic_query


def test_elastic_query_count():
    res = elastic_query('yijiupi_response', query_type='count', query_body={
        "query": {
            "term": {"originalPlace": "厦门"}
        }
    })
    assert isinstance(res, dict)
    assert 'count' in res.keys()
    assert res['count'] > 0


def test_elastic_count_lespark_logs_without_preshow():
    # 统计拉拉公园每天上传日志总条数(action字段值不为preshow的)
    res = elastic_query('lespark_user_action', query_type='count', query_body={
        "query": {
            "bool": {
                "must": {
                    "exists": {
                        "field": "action"
                    }
                },
                "must_not": {
                    "term": {
                        "action": "preshow"
                    }
                }
            }
        }
    })
    return res['count']


def test_elastic_search_lespark_logs_count_group_by_action():
    # 每天上传日志中各行为的条数
    res = elastic_query('lespark_user_action',
                        query_type='search', query_body={
                            "size": 0,
                            "aggs": {
                                "group_by_action": {
                                    "terms": {
                                        "field": "action"
                                    }
                                }
                            }
                        })
    assert 'aggregations' in res
    assert 'group_by_action' in res['aggregations']
    assert 'buckets' in res['aggregations']['group_by_action']
    ans = dict()
    for item in res['aggregations']['group_by_action']['buckets']:
        ans[item['key']] = item['doc_count']
    return ans


def test_elastic_query_search():
    res = elastic_query('yijiupi_response', query_type='search', query_body={
        "query": {
            "term": {"originalPlace": "海口"}
        }
    })
    assert 'hits' in res.keys()
    assert 'total' in res['hits'].keys()
    assert res['hits']['total'] > 0


def test_elastic_query_get_index():
    index = 'changba_response'
    res = elastic_query(index, query_type='mapping',
                        query_body={})
    assert index in res
    assert 'mappings' in res[index]
    assert 'doc' in res[index]['mappings']
    assert 'properties' in res[index]['mappings']['doc']
    assert 'responseTime' in res[index]['mappings']['doc']['properties']


if __name__ == '__main__':
    # test_elastic_query_count()
    # test_elastic_query_search()
    # print(test_elastic_count_lespark_logs_without_preshow())
    # print(test_elastic_search_lespark_logs_count_group_by_action())
    test_elastic_query_get_index()
