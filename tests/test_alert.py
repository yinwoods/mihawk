from mihawk.common.alert import send_sms


def test_send_sms():
    send_sms('haha', '15652375651')


if __name__ == '__main__':
    test_send_sms()
