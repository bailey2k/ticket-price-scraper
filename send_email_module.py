# send_email_module.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cfg import settings

EMAIL_USERNAME = settings.email_from
EMAIL_PASSWORD = settings.email_password

def send_email(subject, content, recipient_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))

    try:
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, recipient_email, msg.as_string())
            print('Email sent successfully')
            server.quit()
    except Exception as e:
        print(f'Error: Email failed to send. {e}')
        server.quit
