from django.core.mail import send_mail
import uuid
from django.conf import settings


def send_forget_password_mail(email, token):
    subject = 'your forgot password link'
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(message)
    print(email_from)
    print(email)
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_set_password_mail(email, token):
    subject = f'your set password link for this {email}'
    message = f'Hi, click on the link to set your password http://127.0.0.1:8000/set_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
