import logging
from ..objects import baseobjects
from ..functions import configurations
from ..functions import maths
import yaml 

class Building(baseobjects.Baseobject):
    def __init__(self,gen,building):
        """
        gen = a dict of the object that generated the building
        building = a dict of the building to be generated
        """
        super().__init__()
        self.label = "building"
        self.generated_by = gen
        self.conf = building
        if self.conf.get('name') == None:
            self.name = self.conf['type']
        else:    
            self.name = self.conf['name']
        
    def get_owned_by(self):
        edge = {
            "node1": self.generated_by['objid'],
            "node2": self.objid,
            "label": "owns",
        }
        return edge

    def get_data(self):
        fund = self.get_fundimentals()
        fund['ownedBy'] = self.generated_by['objid']
        fund['userguid'] = self.generated_by['userguid']
        for k in self.conf.keys():
            fund[k] = self.conf[k]
        return fund
    

def get_faction_pop_structures(c):
    """
    for each structure, returns the faction and pop that owns it. Result is a list of dicts.
    """
    building_query = f"""
    g.V().has('label','faction').as('faction').in('isIn').has('label','pop').as('pop').out('owns').as('structure').path().by(valueMap())
    """
    c.run_query(building_query)
    faction_res = c.query_to_dict(c.res)
    logging.info(f"EXOADMIN: number of items: {len(faction_res)}")
    # Here we are attaching `structure` to the message so that the EventHub trigger can catch it and process it. 
    for item in faction_res:
        item['action'] = 'structure'
    return faction_res

def construct_building(c,message):
    logging.info(f"EXOADMIN: Constucting a building")
    logging.info(f"EXOADMIN: {message}")
    to_build = yaml.safe_load(message['action']['to_build'])
    building = Building(message['agent'],to_build)
    data = {"nodes": [building.get_data()], "edges": [building.get_owned_by()]}
    c.upload_data(message['agent']['userguid'], data)

def augemt_faction(c, message):
    faction = message['faction']
    augment = yaml.safe_load(message['structure']['faction_augments'])
    for item in augment.keys():
        old_value = faction.get(item,0)
        new_value = float(old_value) + float(augment[item])
        if new_value < 0:
            new_value = 0
        logging.info(f"EXOADMIN: {item} has changed from {old_value} to {new_value}")
        c.patch_property(faction['objid'], item, new_value)
    return augment  

def augment_resources(c,resource,value):
    old_volume = float(resource['volume'])
    new_volume = float(resource['volume']) + float(value)
    if new_volume < float(resource['max_volume']):
        if new_volume < 0:
            new_volume = 0
    if new_volume >= float(resource['max_volume']):
        new_volume = float(resource['max_volume'])
    
    logging.info(f"EXOADMIN: resources {resource['name']}:{resource['objid']} changed by {value}, {old_volume}-> {new_volume}")
    c.patch_property(resource['objid'], 'volume', new_volume)


def generate_new_resource(c,resource,location,value,resource_config):
    new_resource = resource_config['resource']['resources'][resource]
    new_resource['label'] = 'resource'
    new_resource['objid'] = maths.uuid()
    if 'max_volume' not in new_resource.keys():
        new_resource['max_volume'] = 100
    if value < 0:
        value = 0
    new_resource['volume'] = value
    data = {'nodes': [new_resource], 'edges': [{'node1': location['objid'], 'node2': new_resource['objid'], 'label': 'has'}]}
    logging.info(f"EXOADMIN: resources {new_resource['name']}:{new_resource['objid']} with volume: {value}")
    logging.info(f"EXOADMIN: Data Created : {data}")
    c.upload_data(location['userguid'], data)
    logging.info(f"EXOADMIN: New nodes : {len(data['nodes'])}. New edges : {len(data['edges'])}")
    return resource

def process_structure(c,message):
    popobjid = message['pop']['objid']
    logging.info(f"EXOADMIN: process_structure, structure: {message['structure']['name']}: {message['structure']['objid']}")
    resource_config = configurations.get_resource_configurations()
    if message['structure'].get('faction_augments'):
        logging.info(f"EXOADMIN: this structure augments a property of the faction")
        augemt_faction(c, message)
    if message['structure'].get('renews_location_resource'):
        logging.info(f"EXOADMIN: this structure renews the resources of the location")
        resources_to_renew = yaml.safe_load(message['structure']['renews_location_resource'])
        location_resources_query = f"g.V().has('objid','{popobjid}').out('inhabits').out('has').has('label','resource').valueMap()"
        location_query = f"g.V().has('objid','{popobjid}').out('inhabits').valueMap()"
        c.add_query(location_resources_query)
        c.add_query(location_query)
        c.run_queries()
        location_resources = c.clean_nodes(c.res[location_resources_query])
        location = c.clean_nodes(c.res[location_query])[0]
        logging.info(f"EXOADMIN: location_resources:{location_resources}")
        for r in resources_to_renew.keys():
            # check if the resource is in the location
            resource_exists = len([i for i in location_resources if i['name']==r])>0
            if resource_exists:
                resource = [i for i in location_resources if i['name']==r][0]
                value = resources_to_renew[r]
                augment_resources(c,resource, value)
            if not resource_exists:
                print(f"EXOADMIN: resource [{r}] not found in location, and will be created")
                generate_new_resource(c,r,location,resources_to_renew[r],resource_config)

    if message['structure'].get('consumes_location_resource'):
        logging.info(f"EXOADMIN: this structure consumes the resources of the location")

    if message['structure'].get('renews_faction_resource'):
        logging.info(f"EXOADMIN: this structure renews the resources of the faction")
        resources_to_renew = yaml.safe_load(message['structure']['renews_faction_resource'])
        faction = message['faction']
        logging.info(f"EXOADMIN: resources_to_renew: {resources_to_renew}. For faction: {faction}")
        faction_resources_query = f"g.V().has('objid', '{faction['objid']}').out('has').valueMap()"
        c.add_query(faction_resources_query)
        c.run_queries()
        faction_resources = c.clean_nodes(c.res[faction_resources_query])
        logging.info(f"EXOADMIN: faction_resources: {faction_resources}")
        faction = message['faction']
        for r in resources_to_renew.keys():
            resource_exists = len([i for i in faction_resources if i['name']==r])>0
            if resource_exists:
                resource = [i for i in faction_resources if i['name']==r][0]
                value = resources_to_renew[r]
                augment_resources(c,resource, value)
            if not resource_exists:
                print(f"EXOADMIN: resource [{r}] not found at faction, and will be created")
                generate_new_resource(c,r,faction,resources_to_renew[r],resource_config)

    if message['structure'].get('each_population_augments_once'):
        logging.info(f"EXOADMIN: this structure augments an attribute of each population in this faction, but only one time")

    if message['structure'].get('each_population_augments_on_cycle'):
        logging.info(f"EXOADMIN: this structure augments an attribute of each population in this faction")


def build_ship(c,message):
    pass

def check_faction_has_shipyard(c,building):
    faction_buildings_query = f"g.V().has('objid','{building['owner']}').out('isIn').in('isIn').out('owns').values('type')"
    c.run_query(faction_buildings_query)    
    has_shipyard = ('shipyard' in c.res)
    return has_shipyard

def validate_building_can_take_action(c,message):
    """
    check if the building can take the action. 
    """
    response = {}
    response['result'] = True
    agent = message['agent']
    if message['action'] == 'build_ship':
        if check_faction_has_shipyard(c,agent):
            return response
        else:
            response['result'] = False
            response['message'] = "Faction does not have a shipyard"        
    return response