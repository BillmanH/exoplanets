from app.models import CosmosdbClient
from django.http import JsonResponse

from app.creators import homeworld
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
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
    return JsonResponse(response)



def get_pop_actions(request):
    c = CosmosdbClient()
    request = dict(request.GET)
    response = {}
    query = f"g.V().has('objid','{request.get('objid','')[0]}').outE('hasAction').inV().valuemap()"
    c.run_query(query)
    res = c.clean_nodes(c.res)
    if len(res)>0:
        response["actions"] = res
    else:
        response["error"] = "no actions returned"
    return JsonResponse(response)

def validate_action(pop,action):
    # Validate that the population is capable of the action
    # pop is ilde and can take action
    if pop['isIdle'].lower() == 'false':
        return False
    # action requires attribute using 'requires_attr'
    if action.get('requires_attr',False):
        req = action['requires_attr'].split(';')
        # Population does not have attribute
        if pop.get(req[0],False):
            if pop[req[0]] >= float(req[1]):
                # Population does have high enough attr
                return True
    return False

def create_job(pop,action,universalTime):
    if type(universalTime)==list:
        universalTime = universalTime[0]
    time_to_complete = int(universalTime['currentTime']) + int(action['effort'])
    actionKeys = [a for a in list(action.keys()) if a not in ['objid','type']]
    popToAction = {"node1":pop['objid'],
                    "node2":action['objid'],
                    "label":"takingAction",
                    "name":"takingAction",
                    'weight':time_to_complete ,
                    "actionType":action['type'],
                    "status":"pending"}
    for a in actionKeys:
        popToAction[a] = action[a]
    edges = [popToAction]
    return edges

 
def take_action(request):
    request = ast.literal_eval(request.GET['values'])
    agent = request["agent"]
    action = request["action"]
    # define queries
    # g.V().has('objid','0000000000').property('isIdle','true')
    # get output
    response = {}
    #### Phase : validate action
    if validate_action(agent,action):
        c = CosmosdbClient()
        setIdle = f"g.V().has('objid','{agent['objid']}').property('isIdle','false')"
        getTime = "g.V().hasLabel('time').valueMap()"
        response['result'] = 'valid: Pop is able to take action'
        c.run_query(getTime)
        universalTime = c.clean_nodes(c.res)
        data = {"nodes": [], "edges": create_job(agent,action,universalTime)}
        c.upload_data(agent['username'], data)
        response["uploadresp"] = str(c.res)
        setIdleResp = c.run_query(setIdle)
        response["setIdleResp"] = str(setIdleResp)
    else:
        response['error'] = "action validation failed"
        response['result'] = 'valid: Pop is not to take action'
        error = JsonResponse(response).status_code = 403
        return error
    return JsonResponse(response) 

def get_all_actions(request):
    query = f"""
    g.E().haslabel('takingAction')
        .has('status',within('pending','resolved')).as('job')
            .outV().has('username','{request.get('username','')[0]}').as('agent')
        .out('enhabits').as('location')
        .path().by(values('name','status','weight','comment').fold())
            .by(values('name').fold())
            .by(values('name','class','objtype').fold())
    """
    c = CosmosdbClient()
    c.run_query(query)
    return c.query_to_dict(c.res)
    