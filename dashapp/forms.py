from django import forms

# ToDo: Make additional validators, if needed. Labels, if needed. Widgets

# General forms

class LoginForm(forms.Form):
    login = forms.CharField(label="Enter your username")
    password = forms.CharField(widget=forms.PasswordInput, label="Enter your password")


class RegisterForm(forms.Form):
    pass
    # login = forms.CharField(label="Enter your username")
    # password = forms.CharField(widget=forms.PasswordInput, label="Enter your password")

# Employee forms


# Manager forms



# Test forms

class TestForm1(forms.Form):
    text1 = forms.CharField()

