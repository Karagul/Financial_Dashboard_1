from django import forms
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from dashapp.models import Company


# ToDo: Make additional validators, if needed. Labels, if needed. Widgets

# Choices

GROUPS = (
    (1, Group.objects.get(pk=1)),
    (2, Group.objects.get(pk=2))
)

# General forms

class LoginForm(forms.Form):
    login = forms.CharField(label="Enter your username")
    password = forms.CharField(
        widget=forms.PasswordInput, label="Enter your password"
    )


class CompanyRegisterForm(ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class UserRegisterForm(ModelForm):
    password_repeated = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        label="Repeat password",
    )
    group = forms.ChoiceField(
        choices=GROUPS
    )

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")
        labels = {"email": "Your e-mail",
                  "password": "Password",
                  }
        widgets = {"password": forms.PasswordInput}

    field_order = (
        "username",
        "first_name",
        "last_name",
        "email",
        "password",
        "password_repeated",
    )
