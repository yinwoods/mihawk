from mihawk.snippets import dbapi
from mihawk.models.log_speed import LogSpeed


def test_commit():
    dbapi.commit()


def test_delete():
    dbapi.delete()


def test_latest_record(log_index, table):
    response = dbapi.latest_record(log_index, table)
    print(response.response)
    # assert isinstance(response, dict)
    # assert 'count' in response
    # assert response.get('count') > 0


if __name__ == '__main__':
    test_latest_record('yijiupi_user_action', LogSpeed)
    test_latest_record('changba_response', LogSpeed)
