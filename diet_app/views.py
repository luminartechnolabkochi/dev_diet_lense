from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from diet_app.forms import SignUpForm,OtpVerificationForm,LoginForm,UserProfileForm

from diet_app.models import UserOtp,User

from django.contrib import messages

from random import randint

from django.core.mail import  send_mail

from django.contrib.auth import authenticate,login,logout

def generate_otp(user_id):

    otp = randint(10000,100000)

    otp+=user_id

    return str(otp)



class SignUpView(View):

    template_name = "register.html"

    form_class = SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data = request.POST

        form_instance = self.form_class(form_data)

        if form_instance.is_valid():

            user_instance = form_instance.save(commit=False)

            user_instance.is_active = False

            user_instance.save()

            otp = generate_otp(user_instance.id)

            UserOtp.objects.create(owner=user_instance,otp=otp)

            send_mail(
                "dietlense otp verification",
                f"your ot is {otp}",
                "sajaykannan10@gmail.com",
                ["karthikramesh12345@gmail.com"],
                fail_silently=True
            )

            # logic for sending email
            # phone #333

            messages.success(request,"otp has been send ....")

            return redirect("verify-otp")
        
        messages.error(request,"failed to create account ")
        return render(request,self.template_name,{"form":form_instance})



class OtpVerificationView(View):

    template_name = "otp-verify.html"

    form_class = OtpVerificationForm


    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data = request.POST

        form_instance = self.form_class(form_data)

        if form_instance.is_valid():

            validated_data= form_instance.cleaned_data

            otp = validated_data.get("otp")

            otp_object = get_object_or_404(UserOtp,otp=otp)

            user_object =get_object_or_404(User,username=otp_object.owner)

            user_object.is_verified = True

            user_object.is_active = True

            user_object.save()

            otp_object.delete()

            messages.success(request,"otp has been verified")

            return redirect("signin")

        return redirect("verify-otp")



class SignInView(View):

    template_name = "signin.html"

    form_class = LoginForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data = request.POST

        form_instance = self.form_class(form_data)

        if form_instance.is_valid():

            validated_data= form_instance.cleaned_data

            u_name = validated_data.get("username")

            pwd = validated_data.get("password")

            user_object = authenticate(request,username = u_name,password = pwd)

            if user_object:

                login(request,user_object)

                messages.success(request,"authentication completed")

                return redirect("profile-create")
        
        messages.error(request,"invalid credential")
        
        return render(request,self.template_name,{"form":form_instance})



def calculate_bmr(height_cm, weight_kg, age, activity_level, gender):
   

    # Mifflin–St Jeor Equation
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Gender must be 'male' or 'female'.")

    # Activity multipliers
    activity_multipliers = {
        '1.2': 1.2,          # Little or no exercise
        '1.375': 1.375,            # Light exercise 1-3 days/week
        '1.55': 1.55,          # Moderate exercise 3-5 days/week
        '1.725': 1.725,           # Hard exercise 6-7 days/week
        '1.9': 1.9         # Very hard exercise & physical job
    }

    if activity_level not in activity_multipliers:
        raise ValueError("Invalid activity level. Choose from: sedentary, light, moderate, active, very active.")

    tdee = bmr * activity_multipliers[activity_level]  # Total Daily Energy Expenditure

    return {"BMR": round(bmr, 2), "TDEE": round(tdee, 2)}
   




class UserProfileCreateView(View):

    template_name = "profile-create.html"

    form_class = UserProfileForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data = request.POST

        form_instance = self.form_class(form_data)

        if form_instance.is_valid():

            validated_data = form_instance.cleaned_data

            height = validated_data.get("height")

            weight = validated_data.get("weight")

            age= validated_data.get("age")

            gender = validated_data.get("gender")

            activity_level = validated_data.get("activity_level")           

            tdee=calculate_bmr(height,weight,age,activity_level,gender).get("TDEE")

            print(tdee)

           

        return render(request,self.template_name,{"form":form_instance})
    









           












    
    





# Emailing settings
