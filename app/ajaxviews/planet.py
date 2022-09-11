from app.models import clean_nodes, run_query, c
from django.http import JsonResponse



def get_planet(request):
    """
    given that user has clicked on a planet,
    get the planet info and the info of the surrounding objects.
    """
    request = request.GET
    selected_planet = [dict(request)]
    # if the user clicks on a star we'll just return the object.
    if selected_planet[0]['objtype'][0] == 'star':
        return JsonResponse({"nodes": [clean_nodes(selected_planet)], "links": [], "error":"objtype is star"})
    # some properties cause problems when they are the root node in d3.js
    if 'orbitsId' in selected_planet[0]:
        del selected_planet[0]['orbitsId']
    del selected_planet[0]["x"]
    del selected_planet[0]["y"]
    del selected_planet[0]["vx"]
    del selected_planet[0]["vy"]
    query = f"g.V().has('objid','{request.get('objid','')}').in('orbits').valueMap()"
    res = run_query(c, query)
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
    queryplanet = f"""g.V().hasLabel('planet')
                    .has('objid','{request.get('objid','')[0]}')
                    .in('enhabits').hasLabel('pop').valueMap()
    """
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
        factions = list(dict.fromkeys([i.get('isInFaction') for i in pops]))
        queryfaction = f"g.V().has('objid', within({factions})).valueMap()"
        resfaction = clean_nodes(run_query(c, queryfaction))
        response["factions"] = resfaction
    return JsonResponse(response)

