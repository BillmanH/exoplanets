from django.urls import path

from . import views
from .ajaxviews import planet

## Adding Ajax requests: 
# path("ajax/planet-details", planet.get_planet_details, name="get_planet_details")

urlpatterns = [
    path("", views.index),
    path("", views.index, name="index"),
]
