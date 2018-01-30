from apistar import http
from jinja2 import Template

from mihawk.common import dbapi
from mihawk.common.config import project_config
from mihawk.common.alert import send_mail
from mihawk.common.alert import send_sms


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

    endpoint = params['endpoint']

    # latency_95th/api=/changba/api/recommend
    metric = (params['metric'] + '/' + params['tags'].replace(':', '=')).strip()
    event_infos = dbapi.get_infos_by_endpoint_metric_time(endpoint, metric)
    if len(event_infos) == 0:
        return {'mail': 'not alert', 'sms': 'not alert'}

    event_info = event_infos[0]

    path = project_config['path']

    emails = [user[1] for user in user_infos]
    # phones = [user[2] for user in user_infos]

    with open(f'{path}/templates/alert.tmpl', 'r') as f:
        t = ''.join(f.readlines())
        t = Template(t)

        html_message = t.render(params=event_info)
        emails = ','.join(emails)
        mail_result = send_mail(title, html_message, emails)
        # sms_result = send_sms(params, phones)
        response = {
            'mail': mail_result,
            'sms': 'sms_result'
        }

    return response
