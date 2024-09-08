import logging
from ..objects import baseobjects
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
        for k in self.conf.keys():
            fund[k] = self.conf[k]
        return fund
    

def count_factions(c):
    faction_count_query = f"""
    g.V().has('label','faction').count()
    """
    c.run_query(faction_count_query)
    return c.res[0]

def get_faction_pop_structures(c):
    building_query = f"""
    g.V().has('label','faction').as('faction').in('isIn').has('label','pop').as('pop').out('owns').as('structure').path().by(valueMap())
    """
    c.run_query(building_query)
    faction_res = c.query_to_dict(c.res)
    logging.info(f"EXOADMIN: number of items: {len(faction_res)}")
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


def process_structure(c,message):
    logging.info(f"EXOADMIN: TODO: process_structure")
    pass
