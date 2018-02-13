from mihawk.common import dbapi


def test_get_user_contact_by_tpl_id(tpl_id):
    result = dbapi.get_user_contact_by_tpl_id(tpl_id)
    assert isinstance(result, list)
    assert isinstance(result[0], tuple)
    assert len(result[0]) == 3


def test_get_infos_by_endpoint_metric_time():
    result = dbapi.get_infos_by_endpoint_metric_time('aws-prophet-recom05',
                                                     'latency_95th/api=/changba/api/recommend')
    print(result)


if __name__ == '__main__':
    # test_get_user_contact_by_tpl_id(2)
    test_get_infos_by_endpoint_metric_time()
