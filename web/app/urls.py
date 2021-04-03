from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('galaxymap', views.galaxy_map, name='galaxy_map'),
] 