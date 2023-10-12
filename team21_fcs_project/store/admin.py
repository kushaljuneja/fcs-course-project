from django.contrib import admin

from .models import Category, Product
from django.http import HttpRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    ordering = ('-name',)
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    ordering = ('-title',)
    list_display = ['category', 'image', 'image_alternate', 'created_by','title', 'price',
                    'is_active', 'created', ]
    list_filter = ['is_active', ]
