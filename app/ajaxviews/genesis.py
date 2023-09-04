from app.connectors.cmdb_graph import CosmosdbClient
from app.models import get_home_system
from django.http import JsonResponse

from app.creators import homeworld, universe



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
    graph_data = universe.build_homeSystem(
        request, username
    )

    c.upload_data(username, graph_data)

    response['note'] = 'solar system created'
    response['status'] = 'success'

    res = get_home_system(username)
    response["solar_system"] = res
    return JsonResponse(response)

def build_population(request):
    response = {}
    c = CosmosdbClient()
    form = c.clean_node(dict(request.GET))
    # Javascript concatenates the effuses into a string, so we need to split it
    if "," in form['effuses']:
        form['effuses'] = form['effuses'].split(",")

    username = form.get('owner','')
    
    # get the homeworld
    queryhomeworld = f"g.V().haslabel('planet').has('isHomeworld').has('username','{username}').valueMap()"
    c.add_query(queryhomeworld)
    c.run_queries()

    homeplanet = c.clean_nodes(c.res[queryhomeworld])[0]
    graph_data = homeworld.build_people(form)
    biome = homeworld.build_biome(homeplanet)
    
    graph_data['edges'] = graph_data['edges'] + homeworld.attach_people_to_world(graph_data['nodes'],homeplanet)
    graph_data['nodes'] = graph_data['nodes'] + [biome.get_data()]
    graph_data['edges'] = graph_data['edges'] + [biome.get_biome_edge()]
    
    response = {'pops':[p for p in graph_data['nodes'] if p.get('label')=='pop']}
    response['factions'] = [p for p in graph_data['nodes'] if p.get('label')=='faction']
    response['note'] = 'population created'
    response['status'] = 'success'
    response['homeworldid'] = homeplanet['objid']
    c.upload_data(username, graph_data)

    return JsonResponse(response)