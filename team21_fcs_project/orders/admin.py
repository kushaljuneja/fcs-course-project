from django.contrib import admin
from .models import Order
from django.http import HttpRequest

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        return True
    
    filter = 'billing_status'
    ordering = ('-created', )
    fields = ('user', 'product', 'quantity', 'created', 'total_paid', 'order_key', 'billing_status')
    list_display = ('user', 'product', 'total_paid', 'billing_status')