

from django import forms

from django.contrib.auth.forms import UserCreationForm

from diet_app.models import User,UserProfile,FoodLog

class SignUpForm(UserCreationForm):


    class Meta:

        model=User

        fields =["username","email","password1","password2","phone"]


class OtpVerificationForm(forms.Form):

    otp = forms.CharField()



class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        exclude = ("owner","bmr")




class FoodLogForm(forms.ModelForm):

    class Meta:

        model = FoodLog

        exclude = ("owner","picture","created_at")
        

class FoodLogImageForm(forms.ModelForm):

    class Meta:

        model = FoodLog

        fields = ["picture"]
        