import yaml

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
            data['nodes'].append(i.get_data())
            data['edges'].append({'source':self.objid, 'target':i.objid, 'label':'has'})
        data['nodes'].append(self.get_data())
        return data

    def get_data(self):
        fund = self.get_fundimentals()
        for k,v in self.stats.items():
            fund[k] = v
        fund['type'] = self.type
        return fund


# Actions resolving the construction of ships. 
def place_ship_in_shipyard(c,ship, message):
    objid = message['agent']['objid']
    faction_shipyard = (
        f"g.V().has('objid','{objid}').in('isIn').has('label','pop').out('owns').has('type','shipyard').valueMap()"
    )
    c.run_query(faction_shipyard)
    if len(c.res) == 0:
        print(f"EXOADMIN: No shipyard found for faction {objid}")
        return None
    shipyard = c.clean_nodes(c.res)[0]
    edge = {
        "node1": ship.get_data['objid'],
        "node2": shipyard['objid'],
        "label": "isIn"
    }
    return edge

def expense_ship(c, ship, message):
    # TODO: Implement ship costs
    pass


def fabricate(c, message):
    design = yaml.safe_load(ship_configurations[message['action']['to_build']])
    data = {"nodes": [], "edges": []}
    if design['label'] == "ship":
        ship = Ship(design, ship_configurations)
        data = ship.get_upload_data()
        ship_in_yard = place_ship_in_shipyard(c, ship, message)
        if ship_in_yard != None:
            data.edges.append(ship_in_yard)
    expense_ship(c, ship, message)
    c.upload_data(message['agent']['userguid'], data)
    print(f"EXOADMIN: fabrication complete for ship: {ship.get_data()}")
