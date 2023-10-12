from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_all, name='store_home'),
    path('<int:pk>', views.product_detail, name='product_detail'),
    path('search/search_categories/<int:pk>', views.category_list, name='category_list'),
    path('search/search_products', views.search_products, name='search_products'),
]
