import logging

import django.apps
import django_db_logger
import django_otp
import two_factor
from django.contrib import admin
from django.db.models import Q
from django.http import HttpRequest
from django.utils.html import format_html

from .models import Buyer, CustomLog, Seller

import logging

db_logger = logging.getLogger('db')



@admin.register(CustomLog)
class CustomLogAdmin(admin.ModelAdmin):
    """ Store login logout logs for users """

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    ordering = ('-time',)
    list_display = ('time', 'desc',)

    fields = (
        'time',
        'desc',
    )


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        if obj is None:
            return True
        else:
            if obj.is_superuser:
                db_logger.error(f"Someone tried to delete an admin")
            return not obj.is_superuser

    ordering = ('-created',)
    list_display = (
        'user_name', 'email', 'verification_document', 'user_type',
    )
    list_filter = (
        'user_type',
    )

    readonly_fields = (
        'user_name',
        'email',
        'verification_document',
    )

    fieldsets = (
        ('Credentials', {'fields': ('user_name', 'email',)}),
        ('Verification', {'fields': ('verification_document', 'user_type',)}),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(~Q(user_type=1), Q(is_active=True))


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        if obj is None:
            return True
        else:
            if obj.is_superuser:
                db_logger.error(f"Someone tried to delete an admin")
            return not obj.is_superuser

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def get_queryset(self, request):
        return self.model.objects.filter(Q(is_active=True))

    ordering = ('-created',)
    list_display = (
        'user_name', 'name', 'email',
    )

    readonly_fields = (
        'user_name',
        'name',
        'email',
    )

    fieldsets = (
        ('Credentials', {'fields': ('user_name', 'name', 'email',)}),
    )


admin.site.unregister(two_factor.models.PhoneDevice)
admin.site.unregister(django_otp.plugins.otp_static.models.StaticDevice)
admin.site.unregister(django_otp.plugins.otp_totp.models.TOTPDevice)
admin.site.unregister(django.contrib.auth.models.Group)
admin.site.unregister(django_db_logger.models.StatusLog)


@admin.register(django_db_logger.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False

    list_display = ('colored_msg', 'create_datetime_format')
    list_display_links = ('colored_msg', )

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    colored_msg.short_description = 'Message'

    def create_datetime_format(self, instance):
        return instance.create_datetime.strftime('%Y-%m-%d %X')

    create_datetime_format.short_description = 'Created at'
