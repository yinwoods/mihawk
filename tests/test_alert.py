from mihawk.app import app
from mihawk.common.alert import send_sms
from apistar import TestClient


def test_send_mail():
    client = TestClient(app)
    response = client.get('/alert?status=PROBLEM&time=2018-01-29+17%3A32%3A00&exp_id=3&tags=api%3A%2Fzhulong%2Fpost%2Fapi&tpl_id=0&stra_id=0&endpoint=aws-prophet-recom05&metric=latency_95th&step=1&priority=1')
    assert response.status_code == 200
    for key, value in response.json().items():
        assert value['mail'] == 'Success'
        assert value['sms'] == 'NotImplented'


def test_send_sms():
    send_sms('haha', '15652375651')


if __name__ == '__main__':
    test_send_mail()
    # test_send_sms()
