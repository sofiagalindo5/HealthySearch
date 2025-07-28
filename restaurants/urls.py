from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.fetch_restaurants, name='fetch_restaurants'),
]