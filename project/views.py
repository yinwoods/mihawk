from apistar import http

from mihawk.common import dbapi
from mihawk.common.alert import send_mail


def alert(params: http.QueryParams):

    try:
        assert "endpoint" in params.keys()
        assert "exp_id" in params.keys()
        assert "metric" in params.keys()
        assert "tpl_id" in params.keys()
    except AssertionError as e:
        return {'error': 'endpoint and metric must in params'}

    title = f'{params["endpoint"]} {params["metric"]}报警'

    tpl_id = int(params['tpl_id'])
    exp_id = int(params['exp_id'])
    user_infos = dbapi.get_user_contact_by_tpl_id(tpl_id, exp_id)

    response = dict()

    message = dict()
    message.update({'机器': params['endpoint']})
    message.update({'指标': params['metric']})
    message.update({'标签': params['tags']})

    for name, email, phone in user_infos:
        mail_result = send_mail(title, message, email)
        item = {
            'mail': mail_result,
            'sms': 'NotImplented'
        }
        response.update({name: item})

    return response
