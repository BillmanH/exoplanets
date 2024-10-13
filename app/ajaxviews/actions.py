from app.models.models import CosmosdbClient
from django.http import JsonResponse
import yaml, os
from app.ajaxviews.ui import planetui

# TODO: Must make the action inheret the properties of the action class in time.py
def get_actions_config():
    actions = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/actions.yaml")))
    return actions["actions"]

def get_buildings_config():
    buildings = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/buildings.yaml")))
    return buildings["buildings"]

def get_available_controls(request):
    data = request.GET.dict()
    response = {}
    if data['isIdle']=='true':
        response['actions'] = get_actions(data)
    else:
        response['actions'] = []
    # Does the entity have any buildings?
    response['buildings'] = get_possible_buildings(data)

    return JsonResponse(response)


def get_object_children(request):
    c = CosmosdbClient()
    # prevent misuse by adding a list of inacceptable types
    inacceptable = ['account','form']
    # appending the form to the C object so that I can use it in the function
    c.form = c.clean_node(dict(request.GET))
    # type is used to separate which data query the UI needs. 
    # This allows control without direct queries in the UI.
    label = c.form.get('type','')
    if label in inacceptable:
        return JsonResponse({"error":f"type {label} is forbidden"})
    elif label == 'planet':
        response = planetui.getOrbitingBodies(c)
    elif label == 'faction':
        response = planetui.getPopulations(c)
    elif label == 'pop':
        response = planetui.getPopActions(c)
    else:
        return JsonResponse({"error":f"inacceptable type {label}"})
    return JsonResponse(response)


class ActionValidator:
    def __init__(self,agent, actions):
        self.agent = agent
        # Actions are valid by default
        self.valid_actions = [a for a in actions if a["applies_to"]==agent["objtype"]]
        self.invalid_actions = []

    def invaldiate_action(self,action,reason):
        type = action['type']
        action['rejection'] = reason
        self.invalid_actions.append(action)
        self.valid_actions = [a for a in self.valid_actions if a["type"]!=type]
        
    def check_has_attr(self, action):
        if "requires_attr" in action.keys():
            for req in action['requires_attr'].keys():
                if req not in self.agent.keys():
                    reason = "agent does not have req attribute"
                    self.invaldiate_action(action,reason)
                if action['requires_attr'][req] > 0:
                    if float(self.agent[req]) < float(action['requires_attr'][req]):
                        reason = f"agent {req} is less than the required value: {self.agent[req]} < {action['requires_attr'][req]}"
                        self.invaldiate_action(action,reason)
                if action['requires_attr'][req] < 0:
                    if float(self.agent[req]) > float(action['requires_attr'][req]):
                        reason = f"agent {req} is greater than the required value: {self.agent[req]} > {action['requires_attr'][req]}"
                        self.invaldiate_action(action,reason)

    def validate(self):
        for act in self.valid_actions:
            self.check_has_attr(act)

    
class BuildingValidator:
    def __init__(self,agent, buildings):
        self.agent = agent
        self.buildings = [a for a in buildings.values() if a["owned_by"]==agent["objtype"]]
        
    def check_has_attr(self, building):
        if "requires_attr" in building.keys():
            for req in building['requires_attr'].keys():
                f_req = float(self.agent[req])
                f_build_req = float(building['requires_attr'][req])
                if req not in self.agent.keys():
                    return False 
                # if the builid req is greater than zero, then the agent must have at least that amount
                if f_build_req > 0:
                    if f_req < f_build_req:
                        return False 
                # if the builid req is less than zero, then the agent must have less than that amount
                if f_build_req < 0:
                    if f_req > f_build_req:
                        return False 
        return True

    def validate(self):
        valid_buildings = [build for build in self.buildings if self.check_has_attr(build)]
        return valid_buildings
    
def get_actions(data):
    c = CosmosdbClient()
    agent_id = data.get('objid','ERROR: objid not found')
    actions = get_actions_config()
    c.run_query(f"g.V().has('objid','{agent_id}').valueMap()")
    agent = c.clean_nodes(c.res)       
    agent = agent[0]
    validator = ActionValidator(agent,actions)
    validator.validate()
    return validator.valid_actions


def get_possible_buildings(data):
    building_data = {}
    c = CosmosdbClient()
    objid = data.get('objid','ERROR: objid not found')
    has_buildings = (
        f"g.V().has('objid','{objid}').out('owns').valueMap()"
    )
    c.run_query(has_buildings)
    buildings = c.clean_nodes(c.res)
    if len(buildings) == 0:
        new_buildings = get_buildings_config()
        validator = BuildingValidator(data,new_buildings)
        valid_buildings = validator.validate()
        building_data['possible_buildings'] = valid_buildings
    else:
        building_data['current_buildings'] = buildings
    return building_data
    
