import json
import smtplib
import requests
import base64
import hmac
import arrow
from hashlib import sha1
import uuid
from urllib.parse import quote
from urllib.parse import urlencode
from email.mime.text import MIMEText
from mihawk.common.config import mail_config
from mihawk.common.config import sms_config


def send_mail(title, message, receivers):

    s = smtplib.SMTP()
    s.connect(host=mail_config['smtp_server'],
              port=mail_config['smtp_port'])
    s.starttls()
    s.login(mail_config['username'], mail_config['password'])

    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = f'{title}'
    msg['From'] = mail_config['sender']
    msg['To'] = receivers

    try:
        s.send_message(msg)
        status = 'Success'
    except smtplib.SMTPException as e:
        print(e)
        status = 'Failed'

    s.quit()

    return status


def send_sms(message, receivers):

    access_id = sms_config['access_id']
    access_secret = sms_config['access_secret']
    server_address = sms_config['server_address']

    state = {
        "state": message["status"],
        "host": message["endpoint"],
        "service": message["metric"],
        "item": message["tags"]
    }

    user_params = {
        'Action': 'SingleSendSms',
        'ParamString': json.dumps(state),
        'RecNum': receivers,
        'SignName': '第四范式',
        'TemplateCode': 'SMS_25990449'
    }
    url = compose_url(user_params, access_id, access_secret, server_address)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        print(url)
        response = requests.get(url, headers=headers)
        print(response.json())
        status = 'Success'
    except Exception as e:
        print(e)
        status = 'Failed'
    return status


def percent_encode(string):
    res = quote(string, '')
    res = res.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    return res


def compute_signature(parameters, access_id, access_secret):
    sorted_keys = sorted(parameters.keys())
    canonicalizedQueryString = ''
    for key in sorted_keys:
        value = parameters[key]
        canonicalizedQueryString += '&' + percent_encode(key) + '=' + percent_encode(value)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
    h = hmac.new((access_secret + "&").encode('utf8'), stringToSign.encode('utf8'), sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def compose_url(user_params, access_id, access_secret, server_address):
    parameters = {
        'Format': 'JSON',
        'Version': '2016-09-27',
        'AccessKeyId': access_id,
        'SignatureVersion': '1.0',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'RegionId': 'cn-beijing',
        'Timestamp': str(arrow.utcnow())
    }
    parameters.update(**user_params)
    print(parameters)
    signature = compute_signature(parameters, access_id, access_secret)
    parameters['Signature'] = signature
    url = server_address + "/?" + urlencode(parameters)
    return url
