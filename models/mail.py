import requests
from flask import current_app as app
from flask import url_for
from config import key


def send_simple_message():
    return requests.post(
        app.config['SEND_EMAIL_URL'],
        auth=("api", key.email_key),
        data={"from": app.config['SEND_EMAIL_FROM'],
              "to": ["test@somemail.com"],
              "subject": "Welcome",
              "text": "Testing some Mailgun awesomness!"})


def send(email, subject, body):
    return requests.post(
        app.config['SEND_EMAIL_URL'],
        auth=("api", key.email_key),
        data={"from": app.config['SEND_EMAIL_FROM'],
              "to": [email],
              "subject": subject,
              "html": body})


def send_verify_email(email, tb64):
    url = app.config['BASE_URL'] + url_for('user.email_verify', tb64=tb64)
    body = "Click to verify your email: <a href='{0}'>{0}</a>".format(url)
    send(email, 'Verify Email', body)


def send_password_email(email, tb64):
    url = app.config['BASE_URL'] + url_for('user.forget_password_verify', tb64=tb64)
    body = "Click to reset your password: <a href='{0}'>{0}</a>".format(url)
    send(email, 'Reset Password', body)

