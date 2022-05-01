from django.core.mail import send_mail
from django.conf import settings

HOST = '127.0.0.1:8000' #LOCALHOST

def send_reset_password_token(token, to):
    SUBJECT = 'reset password demo'
    LINK = HOST + f'/reset_password?token={token}'
    BODY = f"to reset your password, click to the link below \n {LINK}"

    send_mail(
        SUBJECT,
        BODY,
        settings.EMAIL_HOST_USER,
        [to]
    )