from django.db import models

class Restaurant(models.Model): 
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    external_id = models.CharField(max_length=100, unique=True)
    categories = models.TextField(blank=True) 

    def __str__(self): 
        return self.name

class MenuItem(models.Model): 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200)
    is_sugar_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Sugar-Free' if self.is_sugar_free else 'Not Sugar-Free'})"









# Create your models here.
