from apistar import http

from mihawk.snippets import dbapi
from mihawk.snippets.alert import send_mail


def alert(params: http.QueryParams):

    try:
        assert "endpoint" in params.keys()
        assert "metric" in params.keys()
        assert "tpl_id" in params.keys()
    except AssertionError as e:
        return {'error': 'endpoint and metric must in params'}

    title = f'{params["endpoint"]} {params["metric"]}报警'
    message = dict(params)
    user_infos = dbapi.get_user_contact_by_tpl_id(params["tpl_id"])
    for email, phone in user_infos:
        mail_result = send_mail(title, message, email)

    # TODO
    # 每个用户一个dict，表示邮件短信是否成功
    response = {
        'mail': mail_result,
        'sms': 'NotImplemented',
    }

    return response
