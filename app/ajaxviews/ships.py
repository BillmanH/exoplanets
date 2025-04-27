from app.connectors.cmdb_graph import CosmosdbClient
from django.http import JsonResponse
import yaml

def get_ship_isin(c,ship):
    """
    get the edge node that shows where the ship is located
    """
    objid = ship.get('objid', '')
    where_is_the_ship_query = f"g.V().has('objid','{objid}').outE('isIn')"
    c.run_query(where_is_the_ship_query)
    shipIsIn = c.clean_nodes(c.res)[0]
    return shipIsIn


def search_for_targets(request):
    """
    search for objects in the system that match a substring
    """
    c = CosmosdbClient()
    response = {}
    request = dict(request.GET)
    ship = yaml.safe_load(request.get('ship', '{}')[0])
    text = request.get('text', [''])[0]
    shipIsIn = get_ship_isin(c,ship)
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
        response["possible_targets"] = c.clean_nodes(c.res)
    else: 
        response["error"] = "search_for_targets: Ship is not in a known object"
    return JsonResponse(response)


def calculate_prelaunch(request):
    """
    calculate:
     * the launch distance and time to target
     * TODO: the fuel cost of breaking orbit
     * TODO: validate that faction has enough fuel to break orbit
     * return costs and confirm launch button
    """
    c = CosmosdbClient()
    total_distance = 0
    response = {}
    request = dict(request.GET)
    ship = yaml.safe_load(request.get('ship', '{}')[0])
    target = yaml.safe_load(request.get('target', '{}')[0])
    shipIsIn = get_ship_isin(c,ship)
    if shipIsIn['inVLabel'] == "building":
        # the pop, which owns the building, which inhabits the planet which isin the system
        location_query = (
            f"""g.V().has('objid','{shipIsIn['inV']}')
                    .in('owns')
                    .out('inhabits')
                    .valueMap()
            """
        )
        c.run_query(location_query)
        origin_location = c.clean_nodes(c.res)[0]
        response["origin_location"] = origin_location
    else: 
        response["error"] = "calculate_prelaunch: Ship is not in a known object"
    
    if target["objtype"] == "planet":
        total_distance = abs(target['orbitsDistance'] - origin_location['orbitsDistance'])
    if target["objtype"] == "moon":
        c.run_query(f"g.V().has('objid','{target['orbitsId']}').valueMap()")
        orbit_planet = c.clean_nodes(c.res)[0]
        response['note'] = f"{target['name']}:{target['orbitsId']} orbits {orbit_planet['name']}:{orbit_planet['objid']}."
        total_distance = abs(orbit_planet['orbitsDistance'] - origin_location['orbitsDistance'])
        response["path"] = f"{origin_location['name']}:{origin_location['objid']} -> {orbit_planet['name']}:{orbit_planet['objid']}"
        # TODO: Arbitrarily dividing the distance by 100 to get a more reasonable number. I should fix this in genesis so that moons orbitdistance is calculated by AU.
        total_distance = total_distance / 100
 
    response['path'] = {'origin':origin_location['objid'],'target':target['objid']}
    response["total_distance"] = round(total_distance, 3)
    return JsonResponse(response)
