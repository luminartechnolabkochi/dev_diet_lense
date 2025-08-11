

from random import randint

otp = randint(10000,100000)






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

    if activity_level.lower() not in activity_multipliers:
        raise ValueError("Invalid activity level. Choose from: sedentary, light, moderate, active, very active.")

    tdee = bmr * activity_multipliers[activity_level.lower()]  # Total Daily Energy Expenditure

    return {"BMR": round(bmr, 2), "TDEE": round(tdee, 2)}


print(calculate_bmr(164,66,22,"1.2","male"))