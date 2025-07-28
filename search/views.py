from django.shortcuts import render 
from django.http import JsonResponse
from restaurants.models import Restaurant
from restaurants.utils import save_yelp_data  # Make sure this function saves restaurants
import geopy
from geopy.geocoders import Nominatim

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="healthy_search", timeout=5)
    loc = geolocator.geocode(location_name)
    if loc:
        return loc.latitude, loc.longitude
    return None, None

def api_search(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    location = request.GET.get("location", "")

    # for "Use My Location"
    if lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return JsonResponse({"error": "Invalid coordinates"}, status=400)

    # manuelly type in city, convert location to lat/lon
    elif location:
        lat, lon = get_coordinates(location)
        if lat is None or lon is None:
            return JsonResponse({"error": "Could not find coordinates for location"}, status=400)

    else:
        return JsonResponse({"error": "Location or coordinates must be provided"}, status=400)

    # Fetch yelp and store in DB
    save_yelp_data(lat, lon)

    # Query DB for nearby results
    results = Restaurant.objects.filter(
        latitude__range=(lat - 0.1, lat + 0.1),
        longitude__range=(lon - 0.1, lon + 0.1)
    ).values("name", "address", "categories")

    return JsonResponse(list(results), safe=False)