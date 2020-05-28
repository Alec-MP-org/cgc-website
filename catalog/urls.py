from django.urls import path
from . import views

urlpatterns = [
    path('', views.flightsheetsearch, name='flightsheetsearch'),
    path('flightsearch/', views.flightsearch, name='flightsearch'),
    path('flightstats/', views.flightstats, name='flightstats'),
    path('flightstats/data/', views.flightdata, name='flightdata'),
]
