from django.urls import path

from . import views
from .ajaxviews import planet, pop, overview, genesis, actions

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_game),
    path("genesis_view", views.genesis, name="genesis"),
    path("galaxymap", views.galaxy_map, name="galaxy_map"),
    path("systemmap", views.system_map, name="system_map"),
    path("systemui", views.system_ui, name="system_ui"),
    path("popuilocal", views.pop_ui_local, name="pop_ui_local"),
    path("populations", views.populations_view, name="populations"),
    path("ajax/refreshaccount", genesis.refreshaccount, name="refreshaccount"),
    path("ajax/genesissystem", genesis.build_solar_system, name="genesissystem"),
    path("ajax/genesispopulation", genesis.build_population, name="genesispopulation"),

    path("ajax/planet", planet.get_planet, name="get_planet"),
    path("ajax/planet-details", planet.get_planet_details, name="get_planet_details"),
    path("ajax/planet-enhabitants", planet.get_planet_enhabitants, name="get_planet_enhabitants"),
    path("ajax/faction-details", pop.get_faction_details, name="get_faction_details"),
    path("ajax/pops-all", pop.get_all_pops, name="get_all_pops"),

    path("ajax/get-actions", actions.get_actions, name="get_actions"),
    
    path("ajax/take-action", pop.take_action, name="pop_take_action"),
    path("ajax/overview", overview.get_overview, name="overview"),
    path("ajax/newsfeed", overview.get_newsfeed, name="newsfeed")
]
