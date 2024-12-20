from django.core.mail import send_mail
from django.conf import settings

def send_login_email(user_email):
    subject = 'ورود به حساب کاربری'
    message = 'شما با موفقیت وارد حساب کاربری شدید.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
