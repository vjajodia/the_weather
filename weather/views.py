from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    current_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3d4d4d0411ba77a88a6148159d24cd44'
    forcast_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=3d4d4d0411ba77a88a6148159d24cd44'

    cities = City.objects.all()

    if request.method == 'POST': 
        form = CityForm(request.POST) 
        form.save() 


    form = CityForm()

    current_weather_data = []

    for city in cities:

        city_current_weather = requests.get(current_url.format(city)).json() 
        city_forecast_weather = requests.get(forcast_url.format(city)).json()

        weather = {
            'city' : city,
            'temperature' : city_current_weather['main']['temp'],
            'description' : city_current_weather['weather'][0]['description'],
            'icon' : city_current_weather['weather'][0]['icon']
        }

        current_weather_data.append(weather)

    context = {'weather_data' : current_weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) 