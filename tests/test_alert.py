from mihawk.snippets.alert import send_mail


def test_send_mail():
    send_mail(rule_name='1', message='2', receiver='yinchengtao@4paradigm.com')


if __name__ == '__main__':
    test_send_mail()
