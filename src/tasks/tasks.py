import smtplib

from celery import Celery

from config import SMTP_USER, SMTP_PASSWORD

celery = Celery('tasks', broker='redis://localhost:6379')
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

def get_email_template_dashboard(username: str) -> str:
    pass

@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)