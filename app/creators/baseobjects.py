from . import language
from . import maths

class Baseobject:
    def __init__(self):
        self.objid = maths.uuid(n=13)
        self.label = "baseobject"
        self.name = "unnamed"
    def make_name(self,n1,n2):
        return language.make_word(maths.rnd(n1, n2))
    def get_fundimentals(self):
        return {
            "name":self.name,
            "objid":self.objid,
            "label":self.label
        }
    def __repr__(self) -> str:
        return f"<{self.label}: {self.type}; {self.objid}; {self.name}>"