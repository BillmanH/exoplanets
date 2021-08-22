from app.models import clean_node, get_client, run_query
from django.http import JsonResponse


def get_planet(request):
    """
    given that user has clicked on a planet,
    get the planit info and the info of the surrounding objects.
    """
    request = request.GET
    selected_planet = [dict(request)]
    del selected_planet[0]['orbitsId']
    del selected_planet[0]["x"];
    del selected_planet[0]["y"];
    del selected_planet[0]["vx"];
    del selected_planet[0]["vy"];
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
    system = {"nodes": [clean_node(n) for n in nodes], "links": edges}
    return JsonResponse(system)
