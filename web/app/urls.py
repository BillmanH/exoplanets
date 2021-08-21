from django.urls import path

from . import views
from .ajaxviews import planet

urlpatterns = [
    path("", views.index),
    path("explore", views.explore),
    path("new", views.new_universe),
    path("", views.index, name="index"),
    path("galaxymap", views.galaxy_map, name="galaxy_map"),
    path("systemmap", views.system_map, name="system_map"),
    path("ajax/planet", planet.get_planet, name="get_planet")
]
