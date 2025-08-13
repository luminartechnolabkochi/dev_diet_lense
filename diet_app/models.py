from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    phone = models.CharField(max_length=20)

    is_verified = models.BooleanField(default=False)


class UserOtp(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    otp = models.CharField(max_length=12,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
     




class UserProfile(models.Model):

    height = models.FloatField()

    weight = models.FloatField()

    age = models.PositiveIntegerField()

    GENDER_OPTIONS=(
        ("male","male"),
        ("female","female")
    )

    gender = models.CharField(max_length=200,choices=GENDER_OPTIONS,default="male")


    ACTIVITY_CHOICES=(
        ("1.2","Sedentary (little/no exercise)"),
        ("1.375","Lightly active (exercise 1-3 days/week)"),
        ("1.55","Moderately active (exercise 3-5 days/week)"),
        ("1.725","Very active (exercise 6-7 days/week)"),
        ("1.9","Extra active (very intense activity)")
    )


    activity_level = models.CharField(max_length=200,choices=ACTIVITY_CHOICES,default="1.2")

    bmr = models.FloatField(null=True)

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")



# FoodLog 
# [id,name,
#   meal_type,calories,
#   serving_size,
#   note,picture,
#   owner,created_at
# ]

class FoodLog(models.Model):

    name = models.CharField(max_length=200,null=True)

    MEAL_TYPE_OPTIONS=(
        ("breakfast","Breakfast"),
        ("lunch","Lunch"),
        ("dinner","Dinner"),
        ("snack","Snack")
    )

    meal_type = models.CharField(max_length=200,choices=MEAL_TYPE_OPTIONS,null=True)

    calories = models.PositiveIntegerField(null=True)

    serving_size = models.CharField(max_length=200,null=True)

    notes = models.TextField(null=True)

    picture = models.ImageField(upload_to="foodlogs",null=True)

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="foodentries")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name









