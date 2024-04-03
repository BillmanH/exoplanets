from ..objects import baseobjects

class Creature(baseobjects.Baseobject):
    def __init__(self):
        super().__init__()
        self.label = "creature"

    def get_fundimentals(self):
        return {"name": self.name, "objid": self.objid, "label": self.label}


class Species(baseobjects.Baseobject):
    def __init__(self, data):
        super().__init__()
        self.config = data
        if "objid" in data.keys():
            # if there is an objid then this is a copy of an existing object
            self.conformity = .5
            self.aggression = .5
            self.literacy = .5
            self.constitution = .5
            if data['name'] != 'worldgenform':
                self.uuid = data["objid"]
                self.objid = data["objid"]
                self.name = data["name"]
            if data['name'] == 'worldgenform':
                self.name = self.make_name(1, 2)
            self.consumes = data["consumes"]
            self.effuses = data["effuses"]
            
        else: 
            self.conformity = data["conformity"]
            self.aggression = data["aggression"]
            self.literacy = data["literacy"]
            self.constitution = data["constitution"]
            self.name = self.make_name(1, 2)
            self.consumes = data['consumes']
            self.effuses = data['effuses']
        self.label = "species"
        self.pop_std = 0.2 * (1 - float(self.conformity))


    
    def get_data(self):
        fund = self.get_fundimentals()
        fund["consumes"] = self.consumes
        if type(self.effuses)==list:
            fund["effuses"] = ','.join(self.effuses)
        else:
            fund["effuses"] = self.effuses
        if 'uesrguid' in self.config.keys():
            fund['uesrguid'] = self.config['uesrguid']
        fund["conformity"] = self.conformity
        fund["aggression"] = self.aggression
        fund["literacy"] = self.literacy
        fund["constitution"] = self.constitution
        return fund
