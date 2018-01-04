from mihawk.common import dbapi
from mihawk.models.mihawk import LogSpeed


def test_latest_record(log_index, table):
    response = dbapi.latest_record(log_index, table)
    assert isinstance(response, dict)
    assert 'count' in response
    assert response.get('count') > 0


def test_get_user_contact_by_tpl_id(tpl_id):
    result = dbapi.get_user_contact_by_tpl_id(tpl_id)
    assert isinstance(result, list)
    assert isinstance(result[0], tuple)
    assert len(result[0]) == 3


if __name__ == '__main__':
    # test_latest_record('yijiupi_user_action', LogSpeed)
    test_latest_record('changba_response', LogSpeed)
    test_get_user_contact_by_tpl_id(2)
