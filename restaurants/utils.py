from .models import Restaurant, MenuItem
from .yelp_client import search_yelp

def save_yelp_data(lat, lon):
    data = search_yelp(lat, lon)
    for biz in data.get("businesses", []):
        yelp_id = biz["id"]
        name = biz["name"]
        address = ", ".join(biz["location"]["display_address"])
        latitude = biz["coordinates"]["latitude"]
        longitude = biz["coordinates"]["longitude"]
        categories = ", ".join([c["title"] for c in biz["categories"]])

        # Create or update the restaurant
        restaurant, created = Restaurant.objects.get_or_create(
            external_id=yelp_id,
            defaults={
                "name": name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "categories": categories
            }
        )

        # Adds sugar-free tag
        if any(kw in categories.lower() for kw in ["sugar-free", "no sugar added", "health", "keto", "diet"]):
            MenuItem.objects.get_or_create(
                restaurant=restaurant,
                name="Sugar-Free Option",
                is_sugar_free=True
            )

            