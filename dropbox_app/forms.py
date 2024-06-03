from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput()
    )


class FileUploadForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    file = forms.FileField(required=True)
    

class GenerateLinkForm(forms.Form):
    private = forms.BooleanField(initial=False, required=False)
    user = forms.CharField(max_length=255, required=False)
