from app.models import CosmosdbClient, get_system
from django.http import JsonResponse

from app.creators import homeworld, universe
import ast


def refreshaccount(request):
    response = {}
    request = dict(request.GET)
    username = request.get('owner','')[0]
    c = CosmosdbClient()
    query = f"g.V().has('username','{username}').not(has('label','account')).drop()"
    c.run_query(query)
    response['note'] = 'account was purged'
    response['status'] = 'success'
    return JsonResponse(response)

def build_solar_system(request):
    response = {}
    c = CosmosdbClient()
    request = c.clean_node(dict(request.GET))
    username = request.get('owner','')
    # Create the new system
    universe_nodes, universe_edges = universe.build_homeSystem(
        request, username
    )
    data = {"nodes": universe_nodes, "edges": universe_edges}
    c.upload_data(username, data)

    response['note'] = 'solar system created'
    response['status'] = 'success'

    res = get_system(username)
    response["solar_system"] = res
    return JsonResponse(response)

def build_population(request):
    response = {}
    c = CosmosdbClient()
    form = c.clean_node(dict(request.GET))
    username = form.get('owner','')
    
    # get the homeworld
    queryhomeworld = f"g.V().haslabel('planet').has('isHomeworld').has('username','{username}').valueMap()"
    c.add_query(queryhomeworld)
    c.run_queries()

    homeplanet = c.clean_nodes(c.res[queryhomeworld])[0]
    homeworld_nodes, homeworld_edges = homeworld.build_people(form)
    homeworld_edges = homeworld_edges + homeworld.attach_people_to_world(homeworld_nodes,homeplanet)
    
    response = {'pops':[p for p in homeworld_nodes if p.get('label')=='pop']}
    response['factions'] = [p for p in homeworld_nodes if p.get('label')=='faction']
    response['note'] = 'population created'
    response['status'] = 'success'

    data = {"nodes": homeworld_nodes, "edges": homeworld_edges}
    c.upload_data(username, data)

    return JsonResponse(response)