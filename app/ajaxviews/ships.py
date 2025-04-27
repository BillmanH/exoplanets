from app.connectors.cmdb_graph import CosmosdbClient
from django.http import JsonResponse


def search_for_targets(request):
    """
    search for objects in the system that match a substring
    """
    c = CosmosdbClient()
    response = {}
    request = dict(request.GET)
    ship = request.get('ship', '')
    objid = ship.get('objid', '')
    text = request.get('text', '')
    where_is_the_ship_query = f"g.V().has('objid','{objid}').outE('isIn')"
    c.run_query(where_is_the_ship_query)
    shipIsIn = c.clean_nodes(c.res)[0]
    capText = text.capitalize()
    if shipIsIn['inVLabel'] == "building":
        # the pop, which owns the building, which inhabits the planet which isin the system
        system_query = (
            f"""g.V().has('objid','{shipIsIn['inV']}')
                    .in('owns')
                    .out('inhabits')
                    .out('isIn')
                    .in('isIn')
                    .has('objtype',within('planet', 'moon', 'star'))
                    .has('name', containing('{text}').or(containing('{capText}')))
                    .valueMap()
            """
        )
        c.run_query(system_query)
        system = c.clean_nodes(c.res)

    return JsonResponse(system)
