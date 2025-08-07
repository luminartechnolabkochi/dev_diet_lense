from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from diet_app.forms import SignUpForm,OtpVerificationForm

from diet_app.models import UserOtp,User

from django.contrib import messages

from random import randint

from django.core.mail import  send_mail

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

        return redirect("verify-otp")





           












    
    





# Emailing settings
