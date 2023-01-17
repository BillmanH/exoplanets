from app.models import CosmosdbClient
from django.http import JsonResponse

from app.creators import homeworld
import ast



def set_pop_desires(request):
    # sets both desires and actions
    request = dict(request.GET)
    username = request.get('username')[0]
    pop_query = f"g.V().haslabel('pop').has('username','{request.get('username')[0]}').valuemap()"
    objectives_query = "g.V().hasLabel('objective').valuemap()"
    actions_query = "g.V().hasLabel('action').valuemap()"
    c = CosmosdbClient()
    c.add_query(objectives_query)
    c.add_query(pop_query)
    c.add_query(actions_query)
    c.run_queries()

    pops = c.clean_nodes(c.res[pop_query])
    objectives = c.clean_nodes(c.res[objectives_query])
    actions = c.clean_nodes(c.res[actions_query])
    # # Get the pop desire for those objectives
    desire_edges = homeworld.get_pop_desires(pops,objectives)
    data = {"nodes": [], "edges": desire_edges}
    c.upload_data(username, data)
    # # Set the actions for that POP
    action_edges = homeworld.get_pop_actions(pops,actions)
    action_data = {"nodes": [], "edges": action_edges}
    c.upload_data(username, action_data)
    response = {}
    return JsonResponse(response)


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


def get_pop_desires(request):
    """
    given a specific pop,
    get all of the desires of that pop. 
    """
    response = {}
    request = dict(request.GET)
    query = f"""
    g.V().has('objid','{request.get('objid','')[0]}')
        .outE('desires')
        .inV().dedup()
        .path()
        .by(values('name','objid').fold())
            .by('weight')
            .by(values('type','objid','comment','leadingAttribute').fold())
    """
    c = CosmosdbClient()
    c.run_query(query)
    regular_list = [c.flatten(d['objects']) for d in c.res]
    columns=['name','objid','weight','type','objid','comment','leadingAttribute']
    regular_dict = [{columns[j[0]]:j[1] for j in enumerate(i) if columns[j[0]]!='objid'} for i in regular_list]
    if len(regular_dict)>0:
        response["desires"] = regular_dict
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
    