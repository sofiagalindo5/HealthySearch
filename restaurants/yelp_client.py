import requests 
from django.conf import settings 

def search_yelp(lat, lon, term="healthy", radius=10000, limit=20): 
    headers = { 
        "Authorization": f"Bearer {settings.YELP_API_KEY}"
    } 

    params = { 
        "term": term, 
        "categories": "keto, healthy, healthmarkets, sugar-free, no_sugar_added",
        "latitude": lat, 
        "longitude": lon, 
        "radius": radius, 
        "limit": limit, 
    } 

    url = "https://api.yelp.com/v3/businesses/search"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Yelp API error:", response.status_code, response.json())
        return {"businesses": []}

