from app.models import clean_node, get_client, run_query
from django.http import JsonResponse


def get_planet(request):
    """
    given that user has clicked on a planet,
    get the planit info and the info of the surrounding objects.
    """
    request = request.GET
    planet_name = {}
    selected_planet = [dict(request)]
    query = f"g.V().has('objid',{request.get('objid','')}).in('orbits').valueMap()"
    c = get_client()
    res = run_query(c, query)
    c.close()
    nodes = res + selected_planet
    edges = [
        {"source": i["objid"][0], "target": i["orbitsId"][0], "label": "orbits"}
        for i in nodes
        if "orbitsId" in i.keys()
    ]
    system = {"nodes": [clean_node(n) for n in nodes], "edges": edges}
    return JsonResponse(system)
