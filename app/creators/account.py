from datetime import datetime

from . import maths

class Account:
    def __init__(self, username, get_from_graph=False, c=None) -> None:
        if get_from_graph:
            self.fetch_from_graph(c)
        else:
            self.objid = maths.uuid(n=13)
            self.type = "pre_beta_account"
            self.created = datetime.now()
            self.last_used = datetime.now()
            self.label = "account"
            self.username = username

    def fetch_from_graph(self,c):
        pass

    def get_json(self):
        return {
            "objid": self.objid,
            "label": self.label,
            "type": self.type,
            "username": self.username,
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "last_used": self.last_used.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
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
            updatetime = self.last_used.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            query = f"g.V().has('label','account').has('username','{self.username}').property('last_updated','{updatetime}')"
            c.run_query(query)
        else:
            data = {"nodes":[self.get_json()],"edges":[]}
            c.upload_data(self.username,data)


    def drop_system(self,c):
        query = f"g.V().has('username','{self.username}').not(has('label','account'))"
        c.run_query(query)



