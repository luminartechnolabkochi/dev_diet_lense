

from django import forms

from django.contrib.auth.forms import UserCreationForm

from diet_app.models import User

class SignUpForm(UserCreationForm):


    class Meta:

        model=User

        fields =["username","email","password1","password2","phone"]


class OtpVerificationForm(forms.Form):

    otp = forms.CharField()



class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput())

    