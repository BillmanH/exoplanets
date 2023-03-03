from app.models import CosmosdbClient
from django.http import JsonResponse

from app.creators import homeworld, maths
import ast


def get_local_events(request):
    """
    All events that have `happenedAt` a local
    """
    response = {}
    request = dict(request.GET)
    query_local_events = f"g.V().has('objid','{request.get('location','')[0]}').in('happenedAt').valuemap()"
    c = CosmosdbClient()
    c.run_query(query_local_events)
    response["events"] = c.clean_nodes(c.res)
    return JsonResponse(response)