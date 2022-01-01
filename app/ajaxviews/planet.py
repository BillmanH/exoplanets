from app.models import clean_nodes, get_client, run_query
from django.http import JsonResponse, response


def get_planet(request):
    """
    given that user has clicked on a planet,
    get the planet info and the info of the surrounding objects.
    """
    request = request.GET
    selected_planet = [dict(request)]
    # some properties cause problems when they are the root node in d3.js
    del selected_planet[0]['orbitsId']
    del selected_planet[0]["x"]
    del selected_planet[0]["y"]
    del selected_planet[0]["vx"]
    del selected_planet[0]["vy"]
    query = f"g.V().has('objid','{request.get('objid','')}').in('orbits').valueMap()"
    c = get_client()
    res = run_query(c, query)
    c.close()
    edges = [
        {"source": i["objid"][0], "target": i["orbitsId"][0], "label": "orbits"}
        for i in res
        if "orbitsId" in i.keys()
    ]
    nodes = res + selected_planet
    system = {"nodes": clean_nodes(nodes), "links": edges}
    return JsonResponse(system)

def get_planet_details(request):
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
        c.close()
        response["factions"] = resfaction
    return JsonResponse(response)

