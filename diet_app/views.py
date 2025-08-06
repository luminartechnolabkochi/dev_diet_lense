from django.shortcuts import render,redirect

from django.views.generic import View

from diet_app.forms import SignUpForm

from diet_app.models import UserOtp

from django.contrib import messages

from random import randint

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

            # logic for sending email
            # phone #333

            messages.success(request,"otp has been send ....")

            return redirect("register")
        
        messages.error(request,"failed to create account ")
        return render(request,self.template_name,{"form":form_instance})













    
    


