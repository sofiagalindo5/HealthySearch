from django.shortcuts import render
from django.http import HttpResponse 
from .utils import save_yelp_data 

def fetch_restaurants(request): # hardcoded the loc for now
    lat = 40.7128 
    lon = -74.0060 

    save_yelp_data(lat, lon)

    return HttpResponse("Yelp data fetched and saved!")


# Create your views here.
