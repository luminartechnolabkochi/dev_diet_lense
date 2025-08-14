from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View,TemplateView,FormView

from diet_app.forms import SignUpForm,OtpVerificationForm,LoginForm,UserProfileForm,FoodLogForm

from diet_app.models import UserOtp,User,UserProfile,FoodLog

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
                "sabirsadaru@gmail.com",
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



class SignInView(FormView):

    template_name = "signin.html"

    form_class = LoginForm

    # def get(self,request,*args,**kwargs):

    #     form_instance = self.form_class()

    #     return render(request,self.template_name,{"form":form_instance})
    
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

                return redirect("index" if UserProfile.objects.filter(owner=request.user).exists() else "profile-create")

                
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

            form_instance.instance.owner = request.user

            form_instance.instance.bmr = tdee

            form_instance.save()

            # UserProfile.objects.create(**validated_data,owner=request.user,bmr=tdee)

            messages.success(request,"profile has been created successfully")

            return redirect("index")
        else:
            messages.error(request,"failed to create profile")  

           

        return render(request,self.template_name,{"form":form_instance})
    

class IndexView(View):

    template_name= "index.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)



class ProfileDetailView(View):

    template_name = "profile-detail.html"


    def get(self,request,*args,**kwargs):
        
        if UserProfile.objects.filter(owner=request.user).exists():
            
            qs= UserProfile.objects.get(owner = request.user)

            return render(request,self.template_name,{"profile":qs})
        else:

            messages.error(request,"profile not yet created")

            return redirect("signin")


class FoodLogCeateView(FormView):

    template_name = "food-entry.html"

    form_class = FoodLogForm

    def post(self,request,*args,**kwargs):

        form_data = request.POST

        form_instance = self.form_class(form_data)

        if form_instance.is_valid():
            #either
            
            #validated_data = form_instance.cleaned_data

            # FoodLog.objects.create(**validated_data,owner=request.user)
            
            #or
            form_instance.instance.owner = request.user

            form_instance.save()


            messages.success(request,"food log has been added ")

            return redirect("add-food")

        
        messages.error(request,"failed to add food log")

        return  render(request,self.template_name,{"form":form_instance})


from django.utils import timezone


from django.db.models import Sum

class DailySummaryView(View):

    template_name = "daily-summary.html"

    def get(self,request,*args,**kwargs):

        cur_date=timezone.now().date()

        qs=FoodLog.objects.filter(owner = request.user,created_at__date=cur_date) 

        total_calorie =qs.values("calories").aggregate(total=Sum("calories")).get("total")

        balance = request.user.profile.bmr - total_calorie

        gp=qs.values("meal_type").annotate(total=Sum("calories"))

        print(gp)
                   

        return render(request,self.template_name,{"data":qs,"consumed":total_calorie,"remaining":balance})

       

class FoodLogDeleteView(View):

    def get(self,request,*args,**kwargs):
        
        id = kwargs.get("pk")

        food_log_object = get_object_or_404(FoodLog,id=id)

        food_log_object.delete()        

        messages.success(request," food log has been removed")

        return redirect("daily-summary")


class FoodLogUpdateView(View):

    template_name = "food-log-update.html"

    form_class = FoodLogForm

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        food_log_object = get_object_or_404(FoodLog,id=id)

        form_instance = self.form_class(instance=food_log_object)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data = request.POST

        id = kwargs.get("pk")

        food_log_object = get_object_or_404(FoodLog,id=id)

        form_instance = self.form_class(form_data,instance=food_log_object)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"foo log has been updated")

            return redirect("daily-summary")
        else:

            messages.error(request,"failed to update food log")

            return render(request,self.template_name,{"form":form_instance})












    





           












    
    





# Emailing settings
