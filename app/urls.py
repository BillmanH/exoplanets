from django.urls import path

from .views import core, structures
from .ajaxviews import (planet, 
                        pop, 
                        overview, 
                        genesis, 
                        actions, 
                        resources, 
                        events)

urlpatterns = [
    path("", core.index, name="index"),
    path("new", core.new_game),
    path("genesis_view", core.genesis, name="genesis"),
    path("homesystemui", core.home_system_ui, name="home_system_ui"),
    path("galaxymap", core.galaxy_map, name="galaxy_map"),
    path("systemmap", core.system_map, name="system_map"),
    path("systemui", core.system_ui, name="system_ui"),
    path("popuilocal", core.pop_ui_local, name="pop_ui_local"),
    path("populations", core.populations_view, name="populations"),
    
    path("ajax/refreshaccount", genesis.refreshaccount, name="refreshaccount"),
    path("ajax/genesissystem", genesis.build_solar_system, name="genesissystem"),
    path("ajax/genesispopulation", genesis.build_population, name="genesispopulation"),
    path("ajax/planet", planet.get_planet, name="get_planet"),
    path("ajax/planet-details", planet.get_planet_details, name="get_planet_details"),
    path("ajax/planet-inhabitants", planet.get_planet_inhabitants, name="get_planet_inhabitants"),
    path("ajax/faction-details", pop.get_faction_details, name="get_faction_details"),
    path("ajax/pops-all", pop.get_all_pops, name="get_all_pops"),

    path("ajax/get-actions", actions.get_actions, name="get_actions"),
    path("ajax/get-possible-buildings", actions.get_possible_buildings, name="get_possible_buildings"),
    
    path("ajax/get-local-resources", resources.get_local_resourcses, name="get_local_resourcses"),
    path("ajax/get-local-events", events.get_local_events, name="get_local_events"),
    path("ajax/get-object-children", actions.get_object_children, name="get_object_children"),

    path("ajax/take-action", pop.take_action, name="pop_take_action"),
    path("ajax/take-building-action", pop.take_building_action, name="pop_take_building_action"),
    path("ajax/overview", overview.get_overview, name="overview"),
    path("ajax/newsfeed", overview.get_newsfeed, name="newsfeed"),

    path("structures/new", structures.new_structure, name="new_structure")
]
