from app.connectors.cmdb_graph import CosmosdbClient
from django.http import JsonResponse


from app.objects import time as t
from app.objects import structures
from app.objects import ships
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
        factions = list(dict.fromkeys([i.get('isIn') for i in pops]))
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

# TODO: Migrate to pop object
def create_job(pop,action,utu):
    time_to_complete = int(utu.params['currentTime']) + int(action['effort'])
    action['created_at'] = utu.params['currentTime']
    
    uid = str(maths.uuid())
    action['objid'] = uid
    popToAction = {"node1":pop['objid'],
                    "node2":action['objid'],
                    "label":"takingAction",
                    "name":"takingAction",
                    'weight':time_to_complete ,
                    "actionType":action['type'],
                    "created_at": utu.params['currentTime'],
                    "status":"pending"}
    # TODO: The edge could be irrelivatnt given how events are processed. Investigate and delete if not needed.
    data = {"nodes": [action], "edges": [popToAction]}
    return data


def take_action(request):
    request = ast.literal_eval(request.GET['values'])
    agent = request["agent"]
    action = request["action"]
    c = CosmosdbClient()
    utu = t.Time(c)
    utu.get_current_UTU()
    response = {}
    setIdle = f"g.V().has('objid','{agent['objid']}').property('isIdle','false')"
    response['result'] = 'valid: Pop is able to take action'
    

    data = create_job(agent,action,utu)
    c.upload_data(agent['userguid'], data)
    response["uploadresp"] = str(c.res)
    setIdleResp = c.run_query(setIdle)
    response["setIdleResp"] = str(setIdleResp)
    return JsonResponse(response) 


def pop_construction_action(request):
    request = ast.literal_eval(request.GET['values'])
    agent = request["agent"]
    building = request["building"]
    response = {}
    c = CosmosdbClient()
    utu = t.Time(c)
    utu.get_current_UTU()
    
    response['result'] = 'valid: Pop is able to take action'

    action = {
        "type": "construction",
        "label": "action",
        "comment": f"constructing a {building['name'].replace('_',' ')}",
        "effort":building['effort'],
        "applies_to":agent['objtype'],
        "owned_by":building['owned_by'],
        "building":building['type'],
        "created_at": utu.params['currentTime'],
        "to_build":building
    }

    setIdle = f"g.V().has('objid','{agent['objid']}').property('isIdle','false')"
    c.upload_data(agent['userguid'], create_job(agent,action,utu))
    response["uploadresp"] = str(c.res)
    setIdleResp = c.run_query(setIdle)
    response["setIdleResp"] = str(setIdleResp)

    return JsonResponse(response) 

def get_all_actions(request):
    c = CosmosdbClient()
    query = f"""
    g.E().haslabel('takingAction')
        .has('status',within('pending','resolved')).as('job')
            .outV().has('userguid','{request.get('userguid','')[0]}').as('agent')
        .out('inhabits').as('location')
        .path().by(values('name','status','weight','comment').fold())
            .by(values('name').fold())
            .by(values('name','class','objtype').fold())
    """
    c.run_query(query)
    return c.query_to_dict(c.res)
    
def get_current_action(request):
    # return the current action, when the pop is not idle
    request = ast.literal_eval(request.GET['values'])
    c = CosmosdbClient()
    agent = request['agent']
    query = f"""
    g.V().has('objid','{agent.get('objid','')}').outE().has('status','pending').has('name','takingAction').valueMap()
    """
    c.run_query(query)
    res = c.clean_nodes(c.res)[0]
    response = {'current_action':res}
    return JsonResponse(response) 

def get_building_owner(c,building):
    owner_query = f"g.V().has('objid','{building['objid']}').in('owns').valueMap()"
    c.run_query(owner_query)
    owner = c.clean_nodes(c.res)[0]
    return owner

def remove_building(request):
    """
    remove a building from the planet
    """
    request = ast.literal_eval(request.GET['values'])
    c = CosmosdbClient()
    objid = request['building']['objid']
    query = f"g.V().has('objid','{objid}').drop()"
    c.run_query(query)
    return JsonResponse({'result':f'Building [{objid}] removed'})


def build_ship(c, message):
    # probe is the default ship design. It is always available. 
    if message['agent']['current_design'] == 'probe':
        design_config = ships.ship_configurations['designs']['probe']
        ship = ships.Ship(design_config, ships.ship_configurations['components'])
    utu = t.Time(c)
    utu.get_current_UTU()
    building_owner = get_building_owner(c,message['agent'])
    action = {
        "type": "fabricating",
        "label": "action",
        "comment": f"{building_owner['name']}:{building_owner['objid']} building a {design_config['name'].replace('_',' ')}",
        "effort":ship.stats['build_effort'],
        "building":design_config['type'],
        "faction_costs": ship.stats['build_effort'],
        "created_at": utu.params['currentTime'],
        "to_build":design_config
    }
    setIdle = f"g.V().has('objid','{building_owner['objid']}').property('isIdle','false')"
    job = create_job(building_owner,action,utu)
    c.upload_data(building_owner['userguid'], job)
    setIdleResp = c.run_query(setIdle)
    return job


def building_take_action(request):
    c = CosmosdbClient()
    message = ast.literal_eval(request.GET['values'])
    check = structures.validate_building_can_take_action(c,message)
    if check['result']:
          if message['action'] == 'build_ship':
              job = build_ship(c,message)
              return JsonResponse({'result':'valid: Building can take action',
                                   'job':job})
    else:
        return JsonResponse(check)