from ..functions import language
from ..functions import maths

class Baseobject:
    def __init__(self,conf=None):
        self.config = conf
        self.objid = self.make_uuid()
        self.label = "baseobject"
        self.name = "unnamed"

    def make_uuid(self):
        self.uuid = maths.uuid(n=13)
        return self.uuid
    
    def make_name(self,n1,n2):
        """
        makes a random name that ranges in lenght from `n1` to `n2`
        """
        return language.make_word(maths.rnd(n1, n2))
    
    def get_fundimentals(self):
        return {
            "name":self.name,
            "objid":self.uuid,
            "label":self.label
        }
    def __repr__(self) -> str:
        return f"<{self.label}: {self.type if hasattr(self, 'type') else None}; {self.objid}; {self.name}>"

class NewGame():
    def __init__(self,data):
        self.data = data


    def __repr__(self) -> str:
        return f"<NewGame for: {self.data['username']}>"