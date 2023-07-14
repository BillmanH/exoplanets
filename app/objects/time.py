import datetime
import pandas as pd
import numpy as np
import yaml


class Time:
    """
    c : the `CosmosdbClient` object
    UTU : Universal Time Units, the unit of measurement of time in the game.
    """
    def __init__(self,c):
        self.params = {}
        self.c = c
        self.utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()
        self.actions = None

    def get_current_UTU(self):
        self.c.run_query("g.V().hasLabel('time').valueMap()")
        time = self.c.clean_nodes(self.c.res)[0]
        self.params['currentTime'] = time['currentTime']

    def get_global_actions(self):
        """
        Retrieve a list of the global actions.
        """
        # Autoincrement time by one:
        actions_query = """
            g.V().haslabel('action').as('action')
                        .inE('takingAction').has('status','pending').as('job')
                        .outV().as('agent')
                        .select('action','job','agent')
        """

        self.c.run_query(actions_query)
        self.actions = [self.c.parse_all_properties(i) for i in self.c.res]
        # self.actions = pd.DataFrame(actions)

    def global_ticker(self):
        """
        Increment the time by one. Takes a graph connection `c` and the universal time node `time`.
        """
        # Autoincrement time by one:
        currentTime = self.params['currentTime'] + 1

        updateRes = self.c.run_query(f"""g.V().hasLabel('time')
                                    .property('currentTime', {currentTime})
                                    .property('updatedFrom','azfunction')
                                    .property('updatedAt','{str(self.utc_timestamp)}')
                                """
                                )
        
        return f"currentTime was updated from:{self.params['currentTime']} to: {currentTime}"
 
    def __repr__(self) -> str:
        return f"< time at: {self.utc_timestamp} UTU:{self.params.get('currentTime')} >"

class Action:
    """
    All Actions must have an `Agent` who does the action, 
        an `Action` the thing that is done.
        and a `Job` that is the edge between the two in the graph

    """
    def __init__(self,c,action):
        self.agent = action.agent
        self.action = action.action
        self.job = action.job
        self.c = c
        self.data = {"nodes":[],"edges":[]}

    # TODO: Inherit from a base class
    def uuid(self, n=13):
        return "".join([str(i) for i in np.random.choice(range(10), n)])

    def validate_action_time(time,a):
        '''
        validate that the time to complete the task has passed. 
        Not the same as validation that the action can be taken. 
        If the `takingAction` edge has been applied to the agent `a`, then it is just a check of time completed. 
        '''
        if int(a['weight']) < int(time['currentTime']):
            return True
        else:
            return False

    def resolve_augments_self_properties(self):
        agent = self.agent.copy()
        self_properties = yaml.safe_load(self.action["augments_self_properties"])
        for p in self_properties.keys():
            agent[p] = agent[p] + float(self_properties[p])
        return agent

    def mark_action_as_resolved(self):
        patch_job = f"""
        g.V().has('objid','{self.agent['objid']}')
                .outE('takingAction')
                .has('actionType', '{self.job['actionType']}')
                .has('weight','{self.job['weight']}')
                .property('status', 'resolved')
        """    
        self.c.add_query(patch_job.replace(" ", "").replace("\n", ""))

    def mark_agent_idle(self):
        if 'isIdle' in self.agent.keys():
            idleQuery = f"""
            g.V().has('objid','{self.agent['objid']}').property('isIdle','true')
            """
            self.c.add_query(idleQuery.replace(" ", "").replace("\n", ""))
        
    def make_action_event(self,time):
        """
        Creates both the node and the edge for the action
        """
        node = {
            'objid': f"{self.uuid()}",
            'name':'job',
            'label':'event',
            'text': f"The {self.agent['objtype']} ({self.agent['name']}) has completed {self.job['actionType']}",
            'visibleTo':self.agent['username'],
            'time': time.params['currentTime'],
            'username':'event'
        }
        self.data['nodes'].append(node)
        self.data['edges'].append(
            self.c.create_custom_edge(node,self.agent,'completed')
                .replace(" ", "").replace("\n", "")
                )
        

    def query_patch_properties(self):
        query = f"g.V().has('objid','{self.agent['objid']}')"
        for n in yaml.safe_load(self.action["augments_self_properties"]):
            query += f".property('{n}',{self.agent[n]})"
        self.c.add_query(query.replace(" ", "").replace("\n", ""))

    def add_updates_to_c(self,time):
        self.query_patch_properties()
        self.mark_agent_idle()
        self.mark_action_as_resolved()
        self.make_action_event(time)


    def resolve_action(self):
        if len(self.c.stack)>0:
            self.c.run_queries()
        
        self.c.upload_data(self.agent['username'],self.data)


    def make_action_event_edge(self):
        action_edge = c.create_custom_edge(action_event,agent,'completed')
        

    
    def __repr__(self) -> str:
        return f"< ({self.agent.get('name')}: {self.agent.get('objid')}) -{self.job.get('name')}:{self.job.get('weight')}-> ({self.action.get('name')}) >"