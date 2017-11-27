import smtplib
from email.mime.text import MIMEText
from mihawk.snippets.common import mail_config


def send_mail(*args, **kwargs):
    '''
    发送报警邮件
    :param: dag
    :param: rule_name
    :param: message
    :param: receiver
    '''

    rule_name = kwargs['params']['rule_name']
    message = kwargs['params']['message']
    receiver = kwargs['params']['receiver']

    s = smtplib.SMTP_SSL(host=mail_config['smtp_server'], port=mail_config['smtp_port'])
    s.login(mail_config['username'], mail_config['password'])

    msg = MIMEText(f'<h1>{message}</h1>', 'html', 'utf-8')
    msg['Subject'] = f'{rule_name}报警'
    msg['From'] = mail_config['sender']
    msg['To'] = receiver

    s.send_message(msg)
    s.quit()
