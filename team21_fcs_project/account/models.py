import magic
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, User)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import DocumentFileMimeValidator


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, user_name, name, password, **other_fields)

    def create_user(self, email, user_name, name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide a valid email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('Email Address'), unique=True)
    user_name = models.CharField(_('User Name'), max_length=150, unique=True)
    name = models.CharField(_('Full Name'), max_length=150, blank=True)
    address = models.TextField(_('Home Address'), max_length=150, blank=True, null=True)
    phone_number = models.CharField(_('Phone Number '), max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    otp=models.SmallIntegerField(default=123456)
    created = models.DateTimeField(auto_now_add=True)

    type = (
        (1, 'Buyer only'), 
        (2, 'Buyer + Unverified_Seller'), 
        (3, 'Buyer + Verified_Seller'), 
    )

    user_type = models.IntegerField(choices=type, default=1)
    verification_document = models.FileField(upload_to='verification_documents/', validators=[DocumentFileMimeValidator()])

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User(s)'


class Seller(UserBase):
    class Meta:
        proxy = True
        verbose_name = 'Seller'
        verbose_name_plural = 'Seller(s)'

class Buyer(UserBase):
    class Meta:
        proxy = True
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyer(s)'
    
class CustomLog(models.Model):
    desc=models.TextField(blank=True)
    time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Login - Logout Log'
        verbose_name_plural = 'Login - Logout Log(s)'
