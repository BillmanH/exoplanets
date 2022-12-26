from datetime import datetime

from . import maths

strFormat = r'%Y-%m-%dT%H:%M:%S'
class Account:
    def __init__(self, username, c) -> None:
        self.username = username
        if self.check_account_exists(c):
            self.fetch_from_graph(c)
        else:
            self.objid = maths.uuid(n=13)
            self.type = "pre_beta_account"
            self.created = datetime.now()
            self.last_used = datetime.now()
            self.label = "account"

    def fetch_from_graph(self,c):
        query = f"g.V().has('label','account').has('username','{self.username}').valueMap()"
        c.run_query(query)
        self.objid = c.res[0]['objid'][0]
        self.type = c.res[0]['type'][0]
        self.created = datetime.strptime(c.res[0]['created'][0],strFormat)
        self.last_used = datetime.strptime(c.res[0]['last_used'][0],strFormat)
        self.label = c.res[0]['objtype'][0]


    def get_json(self):
        return {
            "objid": self.objid,
            "label": self.label,
            "type": self.type,
            "username": self.username,
            "created": self.created.strftime(strFormat),
            "last_used": self.last_used.strftime(strFormat),
        }

    def check_account_exists(self,c):
        query = f"g.V().has('label','account').has('username','{self.username}').count()"
        c.run_query(query)
        if int(c.res[0])==0:
            return False
        else:
            return True

    def sync_to_graph(self, c):
        self.last_used = datetime.now()
        if self.check_account_exists(c):
            updatetime = self.last_used.strftime(strFormat)
            query = f"g.V().has('label','account').has('username','{self.username}').property('last_updated','{updatetime}')"
            c.run_query(query)
        else:
            data = {"nodes":[self.get_json()],"edges":[]}
            c.upload_data(self.username,data)


    def drop_system(self,c):
        query = f"g.V().has('username','{self.username}').not(has('label','account'))"
        c.run_query(query)



