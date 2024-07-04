from captcha.fields import CaptchaField
from django import forms
from .models import User
from allauth.account.forms import SignupForm


class CustomUserCreationForm(SignupForm):
    captcha = CaptchaField(label='Капча')
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'image',
            'phone_number',
            'first_name',
            'last_name',
        )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'image',
            'phone_number',
            'first_name',
            'last_name',
        )

