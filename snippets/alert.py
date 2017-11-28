import smtplib
from email.mime.text import MIMEText
from mihawk.snippets.common import mail_config


def send_mail(rule_name, message, receiver):
    '''
    发送报警邮件
    :param: dag
    :param: rule_name
    :param: message
    :param: receiver
    '''

    s = smtplib.SMTP()
    s.connect(host=mail_config['smtp_server'],
              port=mail_config['smtp_port'])
    s.starttls()
    s.login(mail_config['username'], mail_config['password'])

    msg = MIMEText(f'<h1>{message}</h1>', 'html', 'utf-8')
    msg['Subject'] = f'{rule_name}报警'
    msg['From'] = mail_config['sender']
    msg['To'] = receiver

    s.send_message(msg)
    s.quit()
