from app.models import CosmosdbClient
from django.http import JsonResponse
import yaml, os


def get_actions_config():
    actions = yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/actions.yaml")))
    return actions["actions"]

def get_buildings_config():
    buildings = yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/buildings.yaml")))
    return buildings["buildings"]

class ActionValidator:
    def __init__(self,agent, actions):
        self.agent = agent
        self.actions = [a for a in actions if a["applies_to"]==agent["objtype"]]
        

    def check_has_attr(self, action):
        if "requires_attr" in action.keys():
            for req in action['requires_attr'].keys():
                if req not in self.agent.keys():
                    return False  
                if action['requires_attr'][req] > 0:
                    if self.agent[req] < action['requires_attr'][req]:
                        return False 
                if action['requires_attr'][req] < 0:
                    if self.agent[req] > action['requires_attr'][req]:
                        return False 
        return True

    def validate(self):
        valid_actions = [act for act in self.actions if self.check_has_attr(act)]
        return valid_actions
    
class BuildingValidator:
    def __init__(self,agent, buildings):
        self.agent = agent
        self.buildings = [a for a in buildings if a["built_by"]==agent["objtype"]]
        

    def check_has_attr(self, building):
        if "requires_attr" in building.keys():
            for req in building['requires_attr'].keys():
                if req not in self.agent.keys():
                    return False  
                if building['requires_attr'][req] > 0:
                    if self.agent[req] < building['requires_attr'][req]:
                        return False 
                if building['requires_attr'][req] < 0:
                    if self.agent[req] > building['requires_attr'][req]:
                        return False 
        return True

    def validate(self):
        valid_buildings = [build for build in self.building if self.check_has_attr(build)]
        return valid_buildings
    
def get_actions(request):
    response = {}
    c = CosmosdbClient()
    form = c.clean_node(dict(request.GET))
    agent_id = form.get('objid','')
    actions = get_actions_config()

    if agent_id:
        response = {}
        c.run_query(f"g.V().has('objid','{agent_id}').valueMap()")
        agent = c.clean_nodes(c.res)

        if len(agent)==0:
            response["error"] = "agent not found"
            return JsonResponse(response)

        if len(agent)>1:
            response["error"] = "duplicate agents"
            return JsonResponse(response)
        
        agent = agent[0]
        validator = ActionValidator(agent,actions)
        valid_actions = validator.validate()
        if len(valid_actions)>0:
            response['actions'] = valid_actions
        else:
            response['error'] = "no actions returned"
        return JsonResponse(response)
    else:
        response['error'] = "no agent id"
        return JsonResponse(response)
    

def get_possible_buildings(request):
    response = {}
    c = CosmosdbClient()
    form = c.clean_node(dict(request.GET))
    agent_id = form.get('objid','')
    buildings = get_buildings_config()

    if agent_id:
        response = {}
        c.run_query(f"g.V().has('objid','{agent_id}').valueMap()")
        agent = c.clean_nodes(c.res)

        if len(agent)==0:
            response["error"] = "agent not found"
            return JsonResponse(response)

        if len(agent)>1:
            response["error"] = "multiple agents"
            return JsonResponse(response)
        
        agent = agent[0]
        validator = BuildingValidator(agent,buildings)
        valid_buildings = validator.validate()
        if len(valid_buildings)>0:
            response['actions'] = valid_buildings
        else:
            response['error'] = "no valid_buildings returned"
        return JsonResponse(response)
    else:
        response['error'] = "no agent id"
        return JsonResponse(response)
    