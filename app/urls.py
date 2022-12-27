from django.urls import path

from . import views
from .ajaxviews import planet, pop, overview, genesis

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_game),
    path("genesis_view", views.genesis, name="genesis"),
    path("galaxymap", views.galaxy_map, name="galaxy_map"),
    path("systemmap", views.system_map, name="system_map"),
    path("systemui", views.system_ui, name="system_ui"),
    path("populations", views.populations_view, name="populations"),
    path("ajax/refreshaccount", genesis.refreshaccount, name="refreshaccount"),
    path("ajax/genesissystem", genesis.build_solar_system, name="genesissystem"),
    path("ajax/genesispopulation", genesis.build_population, name="genesispopulation"),
    path("ajax/genesis-pop-desire", pop.set_pop_desires, name="genesis_pop_desires"),

    path("ajax/planet", planet.get_planet, name="get_planet"),
    path("ajax/planet-details", planet.get_planet_details, name="get_planet_details"),
    path("ajax/faction-details", pop.get_faction_details, name="get_faction_details"),
    path("ajax/pops-all", pop.get_all_pops, name="get_all_pops"),

    path("ajax/pop-desires", pop.get_pop_desires, name="get_pop_desires"),
    path("ajax/pop-actions", pop.get_pop_actions, name="get_pop_actions"),
    path("ajax/take-action", pop.take_action, name="pop_take_action"),
    path("ajax/overview", overview.get_overview, name="overview"),
    path("ajax/newsfeed", overview.get_newsfeed, name="newsfeed")
]
