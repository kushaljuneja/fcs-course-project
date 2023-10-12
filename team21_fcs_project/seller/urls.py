from django.urls import path

from . import views

app_name = 'seller'

urlpatterns = [
    path('', views.seller_home, name='seller_home'),
    path('become_seller/', views.become_seller, name='become_seller'), 
    path('show_products/', views.show_products, name='show_products'), 
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('add_category/', views.add_category, name='add_category'),
]
