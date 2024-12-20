from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import send_login_email

from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save

@receiver(user_logged_in)
def handle_user_login(sender, request, user, **kwargs):
    send_login_email(user.email)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # ایجاد پروفایل کاربر جدید

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # ذخیره پروفایل بعد از ذخیره کاربر  
