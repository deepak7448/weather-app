from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import signForm, CityForm, forecastForm, feedbackForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import City, forecast, feedback
import requests
import datetime

# Create your views here.


def weather(request):
    return render(request, 'weather/Weather.html')


# @login_required()
def current(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f962a3c1697cfcdcd79e894c1b42db52'
        # urlMap = 'https://open.mapquestapi.com/staticmap/v5/map?key=SmG71tZTSw5l2rXpFspwnYQq7Vy0jJPO&center={},{}&size=@2x'
        cities = City.objects.order_by('name')
        form = CityForm(request.POST or None)
        if request.method == 'POST':
            try:
                if form.is_valid():
                    form.save()
                    return render('current')
            except:
                return HttpResponse("""<script>alert('Successfully Add');
                window.location = "http://127.0.0.1:8000/current";
                </script>
                """)
        else:
            form = CityForm()
        # if request.method == 'POST':  # only true if form is submitted
        #   # add actual request data to form for processing
            #  form = CityForm(request.POST)
            # form.save()  # will validate and save if validate

        # form = CityForm()

        weather_data = []
        for city in cities:
            print(city.id)
            mydate = datetime.datetime.now()
            city_weather = requests.get(url.format(city)).json()
            try:
                Weather = {
                    'city': city,
                    'mydate': mydate,
                    'weather': city_weather["main"]["temp"],
                    'humidity': city_weather['main']['humidity'],
                    # 'clouds': city_weather['clouds']['all'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon'],
                    # 'message': city_weather['sys']['message'],
                    'latitude': city_weather['coord']['lat'],
                    'longitude': city_weather['coord']['lon'],
                    # 'country': city_weather['sys']['country'],
                    'sunrise': datetime.datetime.fromtimestamp(city_weather['sys']['sunrise']).strftime('%m-%d %H:%M:%S'),
                    'sunset': datetime.datetime.fromtimestamp(city_weather['sys']['sunset']).strftime('%m-%d %H:%M:%S'),
                    'pressure': city_weather['main']['pressure'],
                    'temp_min': city_weather['main']['temp_min'],
                    'temp_max': city_weather['main']['temp_max'],
                    'wind_speed': city_weather['wind']['speed'],
                    'deg': city_weather['wind']['deg'],
                }
                weather_data.append(Weather)
            except:
                city.delete()
                return HttpResponse("""<script>alert('Sorry City Name not found with our database');
                window.location = "http://127.0.0.1:8000/";
                </script>
                """)

        context = {'weather_data': weather_data, 'form': form, }
        return render(request, "weather/current.html", context)


def forecast(request):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponse('forecast')
    else:
        form = forecastForm()
    return render(request, 'weather/forecast.html', {'form': form})


def about(request):
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('about')
    else:
        form = feedbackForm()
    return render(request, 'weather/about.html', {'form': form})


def login(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('weather')
        else:
            return render(request, 'registration/login.html', messages.error(
                request, 'username and password did not matched'))
    else:
        return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        form = signForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(
                username=username, email=email, password=password)
            messages.success(request, 'Sign up successfully')
            return redirect('signup')
    else:
        form = signForm()
    return render(request, 'registration/signup.html', {'frm': form})


def logout(request):
    auth.logout(request)
    return redirect('weather')
    
    
    
