import json
import logging
import random
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm
from .models import UserBase

db_logger = logging.getLogger('db')


@login_required
def dashboard(request):
    orders = user_orders(request)

    return render(request, 'account/dashboard/dashboard.html', {'section': 'profile', 'orders': orders})


def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            
            get_usr = request.POST.get('usr')
            #user=request.POST.get('user')
            #usr=UserBase.objects.create(user=user)
            usr = UserBase.objects.get(user_name=get_usr)
            
            if int(get_otp) == usr.otp:
                usr.is_active = True
                usr.save()

                # messages.success(request, f'Account is Created For {usr.username}')
                messages.success(request, f'Account created for {usr.user_name}! Try logging in!')

                db_logger.info(f"User: {usr.user_name}, Registered to FCS store 192.168.3.42")

                return redirect('store:store_home')
            else:
                messages.error(request, f'Wrong OTP!! Try again')
                return render(request, 'account/registration/register.html', {'otp': True, 'usr': usr})
        
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                user = registerForm.save(commit=False)
                
                user.user_name = registerForm.clean_username()
                user.email = registerForm.clean_email()
                user.set_password(registerForm.cleaned_data['password1'])
                user.is_active = False
                
                
                user.otp = random.randint(100000, 999999)
                
               # usr = UserBase.objects.get(user_name=user.user_name)
                #usr=user
                
                #UserOTP.objects.create(user=usr, otp=user_otp)
                message = f"Hello {user.user_name},\nYour OTP is {user.otp}\nThanks!"

                send_mail(
                    "Welcome to FCS_Store - Verify Your Email",
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                
                user.save()
                #messages.success(request, f'Account created for {user.user_name}! Try logging in!')

                db_logger.info(f"User: {user.email}, Applied for Email OTP Verification to Activate Registration")

                # return redirect('store:store_home')
                return render(request, 'account/registration/register.html', {'otp': True, 'usr': user})

            else:
                messages.warning(
                    request, 'Invalid reCAPTCHA. Please try again.')
                return redirect(reverse('account:register'))
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


@login_required
def edit_user(request, pk):
    user = request.user

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'You have edited details of {user.user_name}')

            db_logger.info(f"User with user_name: {user.user_name}, edited their buyer profile information.")

            return redirect('account:dashboard')

    else:
        form = UserEditForm(instance=user)

    return render(request, 'account/dashboard/edit_user.html', {'form': form})
