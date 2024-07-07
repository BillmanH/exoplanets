from ..objects import baseobjects

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
            "node1": self.objid,
            "node2": self.generated_by['objid'],
            "label": "owns",
        }
        return edge

    def get_data(self):
        fund = self.get_fundimentals()
        for k in self.conf.keys():
            fund[k] = self.conf[k]
        return fund
    
