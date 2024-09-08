from ..objects import baseobjects

class Ship(baseobjects.Baseobject):
    def __init__(self):
        super().__init__()
        self.label = "ship"
        self.components = []



    def get_data(self):
        fund = self.get_fundimentals()
        return {"name": self.name, "objid": self.objid, "label": self.label}
    

class Component(baseobjects.Baseobject):
    def __init__(self, params):
        super().__init__()
        self.label = "component"
        self.type = params['type']
        self.name = params['name']
        self.augmnts_ship_stats = params['augmnts_ship_stats']
        self.holds = params['holds']
        



    def get_data(self):
        fund = self.get_fundimentals()
        return {"name": self.name, "objid": self.objid, "label": self.label}