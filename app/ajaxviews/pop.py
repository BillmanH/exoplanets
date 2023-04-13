from app.models import CosmosdbClient
from django.http import JsonResponse

from app.creators import homeworld
from ..functions import maths
import ast




def get_pop_text(request):
    """
    given that user has clicked on a p (population),
    get the pop info.
    """
    response = {}
    request = dict(request.GET)
    planet_query = f"g.V().hasLabel('planet').has('objid','{request.get('objid','')[0]}').in().valueMap()"
    faction_query = f"g.V().has('objid', within({factions})).valueMap()"
    c = CosmosdbClient()
    c.run_query(planet_query, leave_open=True)
    respops = c.clean_nodes(c.res)
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
        factions = list(dict.fromkeys([i.get('isInFaction') for i in pops]))
        c.run_query(faction_query)
        resfaction = c.clean_nodes(c.res)
        response["factions"] = resfaction
    return JsonResponse(response)

def get_faction_details(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('faction').has('objid','{request.get('objid','')[0]}').in().valueMap()"
    c = CosmosdbClient()
    c.run_query(queryplanet)
    respops = c.clean_nodes(c.res)
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
    return JsonResponse(response)

def get_all_pops(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    c = CosmosdbClient()
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('pop').has('username','{request.get('username','')[0]}').valueMap()"
    c.run_query(queryplanet)
    respops = c.clean_nodes(c.res)
    if len(respops)>0:
        response["pops"] = respops
    return JsonResponse(response)


def create_job(c,pop,action,universalTime):
    if type(universalTime)==list:
        universalTime = universalTime[0]
    time_to_complete = int(universalTime['currentTime']) + int(action['effort'])
    action = create_action_node(c,action,pop)
    popToAction = {"node1":pop['objid'],
                    "node2":action['objid'],
                    "label":"takingAction",
                    "name":"takingAction",
                    'weight':time_to_complete ,
                    "actionType":action['type'],
                    "status":"pending"}
    edges = [popToAction]
    return edges

def create_action_node(c,action,agent):
    uid = str(maths.uuid())
    action['objid'] = uid
    vertex = c.create_vertex(action,agent['username'])
    c.run_query(vertex)
    return action


def take_action(request):
    request = ast.literal_eval(request.GET['values'])
    agent = request["agent"]
    action = request["action"]
    response = {}
    c = CosmosdbClient()
    setIdle = f"g.V().has('objid','{agent['objid']}').property('isIdle','false')"
    getTime = "g.V().hasLabel('time').valueMap()"
    response['result'] = 'valid: Pop is able to take action'
    c.run_query(getTime)
    universalTime = c.clean_nodes(c.res)
    data = {"nodes": [], "edges": create_job(c,agent,action,universalTime)}
    c.upload_data(agent['username'], data)
    response["uploadresp"] = str(c.res)
    setIdleResp = c.run_query(setIdle)
    response["setIdleResp"] = str(setIdleResp)

    return JsonResponse(response) 


def take_building_action(request):
    request = ast.literal_eval(request.GET['values'])
    agent = request["agent"]
    building = request["building"]
    response = {}
    c = CosmosdbClient()

    action = {
        "type": f"{building['name']} construction",
        "label": "construction",
        "comment": f"constructing a {building['name']}",
        "effort":building['effort'],
        "applies_to":building['owned_by']
    }

    setIdle = f"g.V().has('objid','{agent['objid']}').property('isIdle','false')"
    getTime = "g.V().hasLabel('time').valueMap()"
    response['result'] = 'valid: Pop is able to take action'
    c.run_query(getTime)
    universalTime = c.clean_nodes(c.res)
    data = {"nodes": [], "edges": create_job(c,agent,action,universalTime)}
    c.upload_data(agent['username'], data)
    response["uploadresp"] = str(c.res)
    setIdleResp = c.run_query(setIdle)
    response["setIdleResp"] = str(setIdleResp)

    return JsonResponse(response) 

def get_all_actions(request):
    query = f"""
    g.E().haslabel('takingAction')
        .has('status',within('pending','resolved')).as('job')
            .outV().has('username','{request.get('username','')[0]}').as('agent')
        .out('inhabits').as('location')
        .path().by(values('name','status','weight','comment').fold())
            .by(values('name').fold())
            .by(values('name','class','objtype').fold())
    """
    c = CosmosdbClient()
    c.run_query(query)
    return c.query_to_dict(c.res)
    