from app.models import run_query,  c
from django.http import JsonResponse




def get_overview(request):
    request = dict(request.GET)
    response = {}
    time_units = run_query(c, query="g.V().hasLabel('time').values('currentTime')")
    totalPops = run_query(c, query=f"g.V().hasLabel('pop').has('username','{request.get('username')[0]}').count()")
    idlePops = run_query(c, query=f"g.V().hasLabel('pop').has('username','{request.get('username')[0]}').has('isIdle','True').count()")

    response = {"time": time_units[0], "population": totalPops[0], "idle_population": idlePops[0]}

    return JsonResponse(response)