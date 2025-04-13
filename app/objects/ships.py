import yaml
import logging

from ..objects import baseobjects
from ..functions import configurations

ship_configurations = configurations.get_ship_configurations()['ship']

class Component(baseobjects.Baseobject):
    def __init__(self, config):
        super().__init__()
        self.label = "component"
        self.config = config
        self.type = config['type']
        self.name = config['name']
    

    def get_data(self):
        fund = self.get_fundimentals()
        for k,v in self.config.items():
            fund[k] = v
        fund['type'] = self.config['type']
        return fund


class Design(baseobjects.Baseobject):
    def __init__(self, config):
        super().__init__()
        self.label = "design"
        self.config = config
        self.type = config['type']
        self.name = config['name']
        self.design_type = config['label']
    

    def get_data(self):
        fund = self.get_fundimentals()
        for k,v in self.config.items():
            fund[k] = v
        fund['type'] = self.config['type']
        fund['label'] = self.label
        return fund


class Ship(baseobjects.Baseobject):
    def __init__(self, design, component_configurations):
        super().__init__()
        self.label = "ship"
        # TODO: Naming for ships
        self.name = design['name']
        self.type = design['type']
        self.design = Design(design)
        self.components = [Component(component_configurations[c]) for c in design['components']]
        self.userguid = design['userguid']
        self.stats = {}
        self.build_stats()
    
    def build_stats(self):
        for i in self.components:
            c = i.get_data()
            if 'augments_ship_stats' in c.keys():
                for k,v in c['augments_ship_stats'].items():
                    if k in self.stats.keys():
                        self.stats[k] += v
                    else:
                        self.stats[k] = v

    
    def get_upload_data(self):
        data = {'nodes':[], 'edges':[]}
        data['nodes'].append(self.design.get_data())
        for i in self.components:
            component = i.get_data()
            component['userguid'] = self.userguid
            data['nodes'].append(component)
            data['edges'].append({'node1':self.objid, 'node2':i.objid, 'label':'has'})
        data['nodes'].append(self.get_data())
        return data

    def get_data(self):
        fund = self.get_fundimentals()
        for k,v in self.stats.items():
            fund[k] = v
        fund['type'] = self.type
        fund['userguid'] = self.userguid
        return fund 


# Actions resolving the construction of ships. 
def place_ship_in_shipyard(c,ship, message):
    objid = message['agent']['objid']
    faction_shipyard_query = (
        f"g.V().has('objid','{objid}').out('isIn').in('isIn').has('label','pop').out('owns').has('type','shipyard').valueMap()"
    )
    c.run_query(faction_shipyard_query)
    if len(c.res) == 0:
        logging.info(f"EXOADMIN: No shipyard found for faction {objid}")
        return None
    shipyard = c.clean_nodes(c.res)[0]
    edge = {
        "node1": ship.get_data()['objid'],
        "node2": shipyard['objid'],
        "label": "isIn"
    }
    logging.info(f"EXOADMIN: placing ship: {ship.objid} in shipyard: {shipyard['objid']}")
    return edge

def expense_ship(c, ship, message):
    logging.info(f"EXOADMIN: expensing a ship: not implemented")
    # TODO: Implement ship costs
    pass

def get_design(message):
    to_build = yaml.safe_load(message['action']['to_build'])
    logging.info(f"EXOADMIN: possible ship designs: {list(ship_configurations['designs'].keys())}")
    logging.info(f"EXOADMIN: ship design to build: {to_build['type']}")
    design = ship_configurations['designs'][to_build['type']]
    design['userguid'] = message['agent']['userguid']
    return design

def fabricate(c, message, commit=True):
    logging.info(f"EXOADMIN: fabricating a ship")
    design = get_design(message)
    design['userguid'] = message['agent']['userguid']
    data = {"nodes": [], "edges": []}
    if design['label'] == "ship":
        ship = Ship(design,ship_configurations['components'])
        logging.info(f"EXOADMIN: created a ship: {ship}")
        data = ship.get_upload_data()
        ship_in_yard = place_ship_in_shipyard(c, ship, message)
        if ship_in_yard != None:
            data['edges'].append(ship_in_yard)
        expense_ship(c, ship, message)
    if len(data['nodes']) > 0:
        if commit:
            c.upload_data(message['agent']['userguid'], data)
        logging.info(f"EXOADMIN: data created: {len(data['nodes'])} nodes and {len(data['edges'])} edges")
        logging.info(f"EXOADMIN: fabrication complete for ship: {ship.get_data()}")
    else:
        logging.info(f"EXOADMIN: No data created created")
    if commit == False:
        return data


