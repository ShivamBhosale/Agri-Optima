import json
import math
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, ImageUploadForm
from .utils import classify_image

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from agri_optima_app.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
import requests
import geocoder
import datetime



def dummy(request):
     # in python
    news_api_key = "6e2b5f090ea281cd38a26fa3c313991a"
    url = "https://api.worldapi.com/reports?term=crops%20in%20canada&limit=20&offset=0&use_nlp=1&api_key="
    response = requests.get(url + news_api_key)
    data = response.json()

    # Extract the data you need
    reports = data.get("reports", [])
    
    # Filter the reports where location_country is equal to "Canada"
    canada_reports = [
        report for report in reports 
        if report.get("location_country") == "Canada" 
        and report.get("tag") in ["society & culture", "business & economics", "science & technology", "politics & government"]
    ]
    
    return render(request, 'agri_optima_app/dummy.html', {'canada_reports': canada_reports})

# Create your views here.
def home(request):
    return render(request,'agri_optima_app/index.html')


# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('profile')
#     else:
#         form = CreateUserForm()

#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get('username')
#                 messages.success(request, 'Account was successfully created for ' + user)
#                 return redirect('login')
#         context = {'form': form}
#         return render(request, 'agri_optima_app/register.html', context)


# # test 
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





# def loginPage(request):
#     if request.user.is_authenticated:
#         return redirect('profile')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')
#             else:
#                 messages.info(request, 'Username or Password is incorrect')


#         context = {}
#         return render(request, 'agri_optima_app/login.html', context)


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
        # Handle the case where no UserInfo object with the specified user_name is found
        pro_pic = 'agri_optima_app/profile_pic/default.jpg'    
    # return render(request, 'agri_optima_app/profile.html',{'pro_pic': pro_pic})


    
    
    api_key = '748d19e21dc8cba8d9f339407498ea21'

    
    def get_weather_data(latitude, longitude):
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}'

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
                city = data['name']
                temperature = math.ceil(data['main']['temp'])
                description =  data['weather'][0]['description']
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


    #=================== News API ===============================

    news_api_key = "6e2b5f090ea281cd38a26fa3c313991a"
    url = "https://api.worldapi.com/reports?term=crops%20in%20canada&limit=20&offset=0&use_nlp=1&api_key="
    response = requests.get(url + news_api_key)
    data = response.json()

    # Extract the data you need
    reports = data.get("reports", [])
    
    # Filter the reports where location_country is equal to "Canada"
    canada_reports = [
    report for report in reports
    if report.get("location_country") == "Canada" 
    and report.get("tag") in ["society & culture", "business & economics", "science & technology", "politics & government"]
    and len(report.get("source_citation_title").split()) < 17
    ]
    classification_result = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            classification_result = classify_image(form.instance.image)
    else:
        form = ImageUploadForm()

    return render(request, 'agri_optima_app/profile.html', {'weather_data': weather_data, 'canada_reports': canada_reports, 'form': form, 'result': classification_result})

    
    # return render(request, 'agri_optima_app/profile.html', {'weather_data':weather_data,'canada_reports': canada_reports})
    # return render(request, 'agri_optima_app/profile.html',{'pro_pic': pro_pic})
    