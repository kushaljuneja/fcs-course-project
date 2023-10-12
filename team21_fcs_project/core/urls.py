"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from two_factor.urls import urlpatterns as tf_urls
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('', include(tf_urls)),
    path('account/', include('account.urls', namespace='account')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('seller/', include('seller.urls', namespace='seller')),
    path('passwordreset', auth_views.PasswordResetView.as_view(
        template_name='account/registration/passwordreset.html'), name='reset_password'),
    path('passwordreset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/registration/passwordresetdone.html'), name='password_reset_done'),
    path("passwordreset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='account/registration/passwordresetconfirm.html'), name='password_reset_confirm'),
    path("passwordreset-complete", auth_views.PasswordResetCompleteView.as_view(
        template_name='account/registration/passwordresetcomplete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
