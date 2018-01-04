import smtplib
from email.mime.text import MIMEText
from mihawk.common.config import mail_config


def send_mail(title, message, receiver):

    s = smtplib.SMTP()
    s.connect(host=mail_config['smtp_server'],
              port=mail_config['smtp_port'])
    s.starttls()
    s.login(mail_config['username'], mail_config['password'])

    msg = MIMEText(f'<h1>{message}</h1>', 'html', 'utf-8')
    msg['Subject'] = f'{title}'
    msg['From'] = mail_config['sender']
    msg['To'] = receiver

    try:
        s.send_message(msg)
        status = 'Success'
    except smtplib.SMTPException as e:
        print(e)
        status = 'Failed'

    s.quit()

    return status
