from app.models import clean_nodes, get_client, run_query
from django.http import JsonResponse, response


def get_pop_text(request):
    """
    given that user has clicked on a pop (population),
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
        c.close()
        response["factions"] = resfaction
    return JsonResponse(response)

