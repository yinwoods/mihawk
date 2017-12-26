from mihawk.snippets.alert import send_mail


def test_send_mail():
    response = send_mail(title='apistar test', message='test', receiver='yinchengtao@4paradigm.com')
    print(response)


if __name__ == '__main__':
    test_send_mail()
