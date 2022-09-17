from app.models import get_client, run_multiple_queries, CosmosdbClient
from django.http import JsonResponse




def get_overview(request):
    request = dict(request.GET)
    response = {}
    c = get_client()

    time_units = run_multiple_queries(c, query="g.V().hasLabel('time').values('currentTime')")
    totalPops = run_multiple_queries(c, query=f"g.V().hasLabel('pop').has('username','{request.get('username')[0]}').count()")
    idlePops = run_multiple_queries(c, query=f"g.V().hasLabel('pop').has('username','{request.get('username')[0]}').has('isIdle','True').count()")

    response = {"time": time_units[0], "population": totalPops[0], "idle_population": idlePops[0]}
    c.close()
    return JsonResponse(response)