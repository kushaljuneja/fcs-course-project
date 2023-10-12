from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import CustomLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    st1 = 'user {} logged in through page {}'.format(user.email, request.META.get('HTTP_REFERER'))
    CustomLog.objects.create(desc=st1)

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    st1 = 'user {} logged in failed through page {}'.format(credentials.get('email'), request.META.get('HTTP_REFERER'))
    CustomLog.objects.create(desc=st1)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    st1 = 'user {} logged out through page {}'.format(user.email, request.META.get('HTTP_REFERER'))
    CustomLog.objects.create(desc=st1)


user_logged_in.connect(log_user_login)
user_logged_out.connect(log_user_logout)
user_login_failed.connect(log_user_login_failed)
