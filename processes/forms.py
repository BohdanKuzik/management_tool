from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input"}),
            "password1": forms.PasswordInput(attrs={"class": "form-input"}),
            "password2": forms.PasswordInput(attrs={"class": "form-input"})
        }
