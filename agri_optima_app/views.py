import json
import math
import requests
import geocoder
import datetime
import joblib
import numpy as np
from sklearn.impute import SimpleImputer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import CreateUserForm, SoilImageUploadForm, PlantImageUploadForm, CropYieldForm
from .utils import classify_image_soil, classify_image_plant
from agri_optima_app.models import UserInfo
from django.http import HttpResponseRedirect

@login_required(login_url='login')
def dummy(request):
    # Fetching news reports related to crops in Canada
    news_api_key = "6e2b5f090ea281cd38a26fa3c313991a"
    url = "https://api.worldapi.com/reports?term=crops%20in%20canada&limit=20&offset=0&use_nlp=1&api_key="
    response = requests.get(url + news_api_key)
    data = response.json()
    reports = data.get("reports", [])
    canada_reports = [
        report for report in reports 
        if report.get("location_country") == "Canada" 
        and report.get("tag") in ["society & culture", "business & economics", "science & technology", "politics & government"]
    ]
    
    return render(request, 'agri_optima_app/dummy.html', {'canada_reports': canada_reports})

def home(request):
    return render(request, 'agri_optima_app/index.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for ' + user)
                return redirect('login')
        
        errors_json = json.dumps(form.errors)
        context = {'form': form ,'errors_json': errors_json}
        return render(request, 'agri_optima_app/register2.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username2')
            password = request.POST.get('password2')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'agri_optima_app/login2.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    user_name = request.user.username
    try:
        user = UserInfo.objects.get(uname=user_name)
        pro_pic = user.profile_pic
    except ObjectDoesNotExist:
        pro_pic = 'agri_optima_app/profile_pic/default.jpg'    
    
    # Fetching weather data based on user's location
    api_key = '748d19e21dc8cba8d9f339407498ea21'

    def get_weather_data(latitude, longitude):
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            city = data['name']
            temperature = math.ceil(data['main']['temp'])
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            feels_like = math.ceil(data['main']['feels_like'])
            wind_speed = math.ceil(data['wind']['speed'])
            date = data['dt']
            date_object = datetime.datetime.fromtimestamp(date)
            formatted_date = date_object.strftime("%b %d %Y")

            return {
                'city': city,
                'temperature': temperature,
                'description': description.title(),
                'humidity': humidity,
                'feels_like': feels_like,
                'wind_speed': wind_speed,
                'date': formatted_date,
                'url': url,
            }
        else:
            return None

    def get_user_location():        
        try:
            g = geocoder.ip('me')
            if g.latlng:
                latitude, longitude = g.latlng
                return latitude, longitude
            else:
                return None, None
        except Exception as e:
            print('Error getting user location:', str(e))
            return None, None

    latitude, longitude = get_user_location()
    if latitude is not None and longitude is not None:
        weather_data = get_weather_data(latitude, longitude)
    else:
        weather_data = None

    # Fetching news reports and handling soil/plant analysis
    news_api_key = "339fcdc7270abe92937c11a3b17558a5"
    url = "https://api.worldapi.com/reports?term=crops%20in%20canada&limit=20&offset=0&use_nlp=1&api_key="
    response = requests.get(url + news_api_key)
    data = response.json()
    reports = data.get("reports", [])
    canada_reports = [
        report for report in reports
        if report.get("location_country") == "Canada" 
        and report.get("tag") in ["society & culture", "business & economics", "science & technology", "politics & government"]
        and len(report.get("source_citation_title").split()) < 17
    ]

    classification_result = None
    classification_result_plant = None
    form = SoilImageUploadForm()
    form_plant = PlantImageUploadForm()
    rf_model = joblib.load('agri_optima_app/templates/agri_optima_app/Canada_Decision_Tree_Model.pkl')
    rf_result = None
    rf_form = CropYieldForm()

    if request.method == 'POST':
        if 'soil_form_submit' in request.POST:
            form = SoilImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                classification_result = classify_image_soil(form.instance.image)
        elif 'plant_form_submit' in request.POST:
            form_plant = PlantImageUploadForm(request.POST, request.FILES)
            if form_plant.is_valid():
                form_plant.save()
                classification_result_plant = classify_image_plant(form_plant.instance.image)
        elif 'rf_form_submit' in request.POST:
            rf_form = CropYieldForm(request.POST)
            if rf_form.is_valid():
                # Extract features from the form
                area = rf_form.cleaned_data['area']
                item = rf_form.cleaned_data['item']
                average_temp = rf_form.cleaned_data['average_temp']
                pesticide_amount = rf_form.cleaned_data['pesticide_amount']
                average_rain = rf_form.cleaned_data['average_rain']

                input_features = [area, item, average_temp, pesticide_amount, average_rain]
                input_features = np.array(input_features).reshape(1, -1)

                imputer = SimpleImputer(strategy='mean')
                input_features_imputed = imputer.fit_transform(input_features)

                # Make predictions using the loaded RandomForest model
                yield_prediction = rf_model.predict(input_features_imputed)

                # Set the result to be displayed in the template
                rf_result = yield_prediction[0]
                


    return render(request, 'agri_optima_app/profile.html', {
        'weather_data': weather_data,
        'canada_reports': canada_reports,
        'form': form,
        'form_plant': form_plant,
        'result': classification_result,
        'result_plant': classification_result_plant,
        'rf_form': rf_form,
        'rf_result': rf_result,
    })


