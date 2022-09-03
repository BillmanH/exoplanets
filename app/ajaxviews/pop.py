from distutils.command.clean import clean
from app.models import clean_nodes, get_client, run_query, upload_data, flatten
from django.http import JsonResponse

from app.creators import homeworld
import ast

def make_homeworld(request):
    request = dict(request.GET)
    # WARNING: user can only have one form. 
    username = request.get('username')[0]
    queryform = f"g.V().has('form','username','{username}').valuemap()"
    queryhomeworld = f"g.V().haslabel('planet').has('isHomeworld').has('username','{username}').valueMap()"
    c = get_client()
    form = clean_nodes(run_query(c, queryform))[0]
    homeplanet = clean_nodes(run_query(c, queryhomeworld))[0]
    homeworld_nodes, homeworld_edges = homeworld.build_people(form)
    homeworld_edges = homeworld_edges + homeworld.attach_people_to_world(homeworld_nodes,homeplanet)
    response = {'pops':[p for p in homeworld_nodes if p.get('label')=='pop']}
    response['factions'] = [p for p in homeworld_nodes if p.get('label')=='faction']
    data = {"nodes": homeworld_nodes, "edges": homeworld_edges}
    upload_data(c, username, data)
    c.close()
    return JsonResponse(response)


def set_pop_desires(request):
    # sets both desires and actions
    request = dict(request.GET)
    c = get_client()
    username = request.get('username')[0]
    poquery = f"g.V().haslabel('pop').has('username','{request.get('username')[0]}').valuemap()"
    objectives = run_query(c, query="g.V().hasLabel('objective').valuemap()")
    pops = run_query(c, query=poquery)
    objectives = clean_nodes(objectives)
    pops = clean_nodes(pops)
    # # Get the pop desire for those objectives
    desire_edges = homeworld.get_pop_desires(pops,objectives)
    data = {"nodes": [], "edges": desire_edges}
    upload_data(c, username, data)
    # # Set the actions for that POP
    actions = clean_nodes(run_query(c, query="g.V().hasLabel('action').valuemap()"))
    action_edges = homeworld.get_pop_actions(pops,actions)
    action_data = {"nodes": [], "edges": action_edges}
    upload_data(c, username, action_data)
    response = {}
    c.close()
    return JsonResponse(response)


def get_pop_text(request):
    """
    given that user has clicked on a p (population),
    get the pop info.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('planet').has('objid','{request.get('objid','')[0]}').in().valueMap()"
    c = get_client()
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
        factions = list(dict.fromkeys([i.get('isInFaction') for i in pops]))
        queryfaction = f"g.V().has('objid', within({factions})).valueMap()"
        resfaction = clean_nodes(run_query(c, queryfaction))
        response["factions"] = resfaction
    c.close()
    return JsonResponse(response)

def get_faction_details(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('faction').has('objid','{request.get('objid','')[0]}').in().valueMap()"
    c = get_client()
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
    c.close()
    return JsonResponse(response)

def get_all_pops(request):
    """
    given that user has clicked on a faction (population),
    get the pop info for the pops in that faction.
    """
    response = {}
    request = dict(request.GET)
    queryplanet = f"g.V().hasLabel('pop').has('username','{request.get('username','')[0]}').valueMap()"
    c = get_client()
    respops = clean_nodes(run_query(c, queryplanet))
    pops = [i for i in respops if i.get("objtype")=='pop']
    # if faction has people, get the factions (only the ones found on that planet)
    if len(pops)>0:
        response["pops"] = pops
    c.close()
    return JsonResponse(response)


def get_pop_desires(request):
    """
    given a specific pop,
    get all of the desires of that pop. 
    """
    response = {}
    request = dict(request.GET)
    query = f"g.V().has('objid','{request.get('objid','')[0]}').outE('desires').inV().dedup().path().by(values('name','objid').fold()).by('weight').by(values('type','objid','comment','leadingAttribute').fold())"
    c = get_client()
    res = run_query(c, query)
    c.close()
    regular_list = [flatten(d['objects']) for d in res]
    columns=['name','objid','weight','type','objid','comment','leadingAttribute']
    regular_dict = [{columns[j[0]]:j[1] for j in enumerate(i) if columns[j[0]]!='objid'} for i in regular_list]
    if len(regular_dict)>0:
        response["desires"] = regular_dict
    return JsonResponse(response)


def get_pop_actions(request):
    request = dict(request.GET)
    response = {}
    query = f"g.V().has('objid','{request.get('objid','')[0]}').outE('hasAction').inV().valuemap()"
    c = get_client()
    res = clean_nodes(run_query(c, query))
    c.close()
    if len(res)>0:
        response["actions"] = res
    else:
        response["actions"] = ["no actions returned"]
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
    actionToTime = {"node1":action['objid'],
                    "node2":universalTime['objid'],
                    "label":"hasJob",
                    "name":"hasJob",
                    "actionType":action['type'],
                    'weight':time_to_complete ,
                    "status":"pending"}
    popToAction = {"node1":pop['objid'],
                    "node2":action['objid'],
                    "label":"takingAction",
                    "name":"takingAction",
                    "actionType":action['type'],
                    "status":"pending"}
    edges = [actionToTime,popToAction]
    return edges

 
def take_action(request):
    request = ast.literal_eval(request.GET['values'])
    agent = request["agent"]
    action = request["action"]
    # define queries
    # g.V().has('objid','0000000000').property('isIdle','true')
    setIdle = f"g.V().has('objid','{agent['objid']}').property('isIdle','false')"
    getTime = "g.V().hasLabel('time').valueMap()"
    # get output
    response = {}
    #### Phase : validate action
    if validate_action(agent,action):
        response['result'] = 'valid: Pop is able to take action'
        c = get_client()
        universalTime = clean_nodes(run_query(c,getTime))
        data = {"nodes": [], "edges": create_job(agent,action,universalTime)}
        upload_data(c, agent['username'], data)
        setIdleResp = run_query(c, setIdle)
        response["setIdleResp"] = setIdleResp
    else:
        response['error'] = "action validation failed"
        response['result'] = 'valid: Pop is not to take action'
        error = JsonResponse(response).status_code = 403
        return error
    return JsonResponse(response) 