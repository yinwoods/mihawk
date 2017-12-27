from mihawk.app import app
from apistar import TestClient


def test_send_mail():
    client = TestClient(app)
    response = client.get('/alert?endpoint=aws-prophet-recom03&status=PROBLEM&stra_id=3&tags=&exp_id=0&metric=cpu.idle&step=8&priority=0&time=2017-12-26+03%3A37%3A00&tpl_id=2')
    assert response.status_code == 200
    for key, value in response.json().items():
        assert value['mail'] == 'Success'
        assert value['sms'] == 'NotImplented'


if __name__ == '__main__':
    test_send_mail()
