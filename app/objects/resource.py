class Resource:
    def __init__(self, conf):
        self.objid = maths.uuid(n=13)
        self.label = "resource"
        self.conf = conf
        self.name = conf["name"]
        self.description = conf["description"]
        self.volume = maths.rnd(conf["mean"],conf["std"], min_val=0)
        if conf.get('replenish_rate'):
            self.replenish_rate = conf['replenish_rate']
        else: 
            self.replenish_rate = None
    def get_data(self):
        fund = {
            "name": self.name,
            "objid": self.objid,
            "label": self.label,
            "volume": self.volume,
            "description": self.description
        }
        if (self.replenish_rate):
            fund['replenish_rate'] = self.replenish_rate
        return fund

    def __repr__(self) -> str:
        return f"<{self.label}: {self.objid}; {self.name}>"  