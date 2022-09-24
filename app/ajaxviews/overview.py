from app.models import CosmosdbClient
from django.http import JsonResponse




def get_overview(request):
    request = dict(request.GET)
    response = {}

    time_units = "g.V().hasLabel('time').values('currentTime')"
    totalPops = f"g.V().hasLabel('pop').has('username','{request.get('username')[0]}').count()"
    idlePops = f"g.V().hasLabel('pop').has('username','{request.get('username')[0]}').has('isIdle','True').count()"

    c = CosmosdbClient()
    c.add_query(time_units)
    c.add_query(totalPops)
    c.add_query(idlePops)
    c.run_queries()

    response = {"time": c.res[time_units][0], "population": c.res[totalPops][0], "idle_population": c.res[idlePops][0]}

    return JsonResponse(response)