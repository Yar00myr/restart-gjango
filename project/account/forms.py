from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        extra_fields = ["email"]
        fields = ["username", "password1", "password2", "email"]


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(label="Email:")
    avatar = forms.ImageField(required=False, label="Upload avatar:")

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email already exists")
        else:
            return new_email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email

class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="login")
    password = forms.PasswordInput()