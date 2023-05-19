from app.models import CosmosdbClient
from django.http import JsonResponse

def get_planet(request):
    """
    given that user has clicked on a planet,
    get the planet info and the info of the surrounding objects.
    """
    c = CosmosdbClient()
    request = request.GET
    selected_planet = [dict(request)]
    # if the user clicks on a star we'll just return the object.
    if selected_planet[0]['objtype'][0] == 'star':
        return JsonResponse({"nodes": [c.clean_nodes(selected_planet)], "links": [], "error":"objtype is star"})
    # some properties cause problems when they are the root node in d3.js
    if 'orbitsId' in selected_planet[0]:
        del selected_planet[0]['orbitsId']
    del selected_planet[0]["x"]
    del selected_planet[0]["y"]
    del selected_planet[0]["vx"]
    del selected_planet[0]["vy"]

    query = f"g.V().has('objid','{request.get('objid','')}').in('orbits').valueMap()"
    c.run_query(query)

    edges = [
        {"source": i["objid"][0], "target": i["orbitsId"][0], "label": "orbits"}
        for i in c.res
        if "orbitsId" in i.keys()
    ]
    nodes =  c.res + selected_planet
    system = {"nodes": c.clean_nodes(nodes), "links": edges}
    return JsonResponse(system)


def get_planet_details(request):
    response = {}
    request = dict(request.GET)
    queryplanet = f"""g.V().hasLabel('planet')
                    .has('objid','{request.get('objid','')[0]}')
                    .valueMap()
    """
    c = CosmosdbClient()
    c.run_query(queryplanet)
    planet = c.clean_nodes(c.res)
    response['planet'] = planet

    return JsonResponse(response)

def get_planet_inhabitants(request):
    response = {}
    request = dict(request.GET)
    queryplanet = f"""g.V().hasLabel('planet')
                    .has('objid','{request.get('objid','')[0]}')
                    .in('inhabits').hasLabel('pop').valueMap()
    """
    c = CosmosdbClient()
    c.run_query(queryplanet)
    respops = c.clean_nodes(c.res)
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
        factions = list(dict.fromkeys([i.get('isIn') for i in pops]))
        queryfaction = f"g.V().has('objid', within({factions})).valueMap()"
        c.run_query(queryfaction)
        resfaction = c.clean_nodes(c.res)
        response["factions"] = resfaction
    return JsonResponse(response)

