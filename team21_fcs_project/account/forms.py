from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserBase

class RegistrationForm(UserCreationForm):
    user_name = forms.CharField(min_length=8, max_length=16)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'password1', 'password2')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower().strip()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError('Please use another username, that is already taken')
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        r = UserBase.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email


class UserEditForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=30)
    address = forms.CharField(label="Address", max_length=30)
    phone_number = forms.RegexField(label="Phone Number", regex=r'^[0-9]{10}$')

    class Meta:
        model = UserBase
        fields = ('name', 'address', 'phone_number')
    
    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address'].lower()
        return address
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number