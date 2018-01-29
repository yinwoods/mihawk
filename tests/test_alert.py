from mihawk.app import app
from mihawk.common.alert import send_sms
from apistar import TestClient


def test_send_mail():
    client = TestClient(app)
    response = client.get('/alert?metric=latency_95th&tpl_id=0&tags=api%3A%2Fzhulong%2Fapi%2Frecommend&exp_id=3&stra_id=0&endpoint=aws-prophet-recom05&status=PROBLEM&step=3&priority=1&time=2017-12-27+06%3A57%3A00 HTTP/1.1')
    assert response.status_code == 200
    for key, value in response.json().items():
        assert value['mail'] == 'Success'
        assert value['sms'] == 'NotImplented'


def test_send_sms():
    send_sms('haha', '15652375651')


if __name__ == '__main__':
    # test_send_mail()
    test_send_sms()
