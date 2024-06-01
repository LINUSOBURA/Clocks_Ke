from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Product

User = get_user_model()


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'details', 'image']
