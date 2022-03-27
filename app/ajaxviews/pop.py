from app.models import clean_nodes, get_client, run_query, upload_data
from django.http import JsonResponse

from app.creators import homeworld

def make_homeworld(request):
    request = dict(request.GET)
    # WARNING: user can only have one form. 
    username = request.get('username')[0]
    queryform = f"g.V().has('form','username','{username}').valuemap()"
    queryhomeworld = f"g.V().haslabel('planet').has('isHomeworld').has('username','{username}').valueMap()"
    c = get_client()
    form = clean_nodes(run_query(c, queryform))[0]
    homeplanet = clean_nodes(run_query(c, queryhomeworld))[0]
    homeworld_nodes, homeworld_edges = homeworld.build_people(form)
    homeworld_edges = homeworld_edges + homeworld.attach_people_to_world(homeworld_nodes,homeplanet)
    response = {'pops':[p for p in homeworld_nodes if p.get('label')=='pop']}
    response['factions'] = [p for p in homeworld_nodes if p.get('label')=='faction']
    data = {"nodes": homeworld_nodes, "edges": homeworld_edges}
    upload_data(c, username, data)
    c.close()
    return JsonResponse(response)

def set_pop_desires(request):
    request = dict(request.GET)
    c = get_client()
    username = request.get('username')[0]
    poquery = f"g.V().haslabel('pop').has('username','{request.get('username')[0]}').valuemap()"
    objectives = run_query(c, query="g.V().hasLabel('objective').valuemap()")
    pops = run_query(c, query=poquery)
    objectives = clean_nodes(objectives)
    pops = clean_nodes(pops)
    # # Get the pop desire for those objectives
    desire_edges = homeworld.get_pop_desires(pops,objectives)
    data = {"nodes": [], "edges": desire_edges}
    upload_data(c, username, data)
    c.close()
    response = {}
    return JsonResponse(response)


def get_pop_text(request):
    """
    given that user has clicked on a p (population),
    get the pop info.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('planet').has('objid','{request.get('objid','')[0]}').in().valueMap()"
    c = get_client()
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
        factions = list(dict.fromkeys([i.get('isInFaction') for i in pops]))
        queryfaction = f"g.V().has('objid', within({factions})).valueMap()"
        resfaction = clean_nodes(run_query(c, queryfaction))
        response["factions"] = resfaction
    c.close()
    return JsonResponse(response)

def get_faction_details(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('faction').has('objid','{request.get('objid','')[0]}').in().valueMap()"
    c = get_client()
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
    c.close()
    return JsonResponse(response)

def get_all_pops(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('pop').has('username','{request.get('username','')[0]}').valueMap()"
    c = get_client()
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
    c.close()
    return JsonResponse(response)