from app.models import CosmosdbClient
from django.http import JsonResponse

from app.creators import homeworld
import ast


def get_local_resourcses(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"""
    g.V().has('objid','{request.get('location','')[0]}')
        .out('has').haslabel('resource').valuemap()
    """
    c = CosmosdbClient()
    c.run_query(queryplanet)
    response["resources"] = c.clean_nodes(c.res)
    return JsonResponse(response)