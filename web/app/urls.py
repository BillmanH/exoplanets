from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('/', views.index),
    path('explore', views.explore),
    path('new', views.new_universe),
    path('', views.index, name='index'),
    path('galaxymap', views.galaxy_map, name='galaxy_map'),
] 