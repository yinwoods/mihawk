from mihawk.common.alert import send_sms
from mihawk.common.alert import send_wechat


def test_send_wechat():
    send_wechat('报警', '内容', 'YinChengTao')


def test_send_sms():
    send_sms('haha', '15652375651')


if __name__ == '__main__':
    test_send_wechat()
    # test_send_sms()
