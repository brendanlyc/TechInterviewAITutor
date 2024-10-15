import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException

import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))
sender_email = config['email']['SENDER_EMAIL']
sender_password = config['email']['SENDER_PASSWORD']
smtp_server = config['email']["SMTP_SERVER"]
smtp_port = int(config['email']['SMTP_PORT'])


def send_reset_email(to_email: str, reset_link: str):
    subject = "Tetor: Password Reset Request"
    body = f"Please click the link below to reset your password.\n\n{reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.starttls()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Reset email sent to {to_email}")
    
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Error sending email")