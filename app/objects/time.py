import datetime
import pandas as pd



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
        actions = self.c.res
        self.actions = pd.DataFrame(actions)

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
        self.agent = self.parse_properties(action.agent)
        self.action = self.parse_properties(action.action)
        self.job = action.job

    def parse_properties(node):
        n = {}
        for k in node["properties"].keys():
            if len(node["properties"][k]) == 1:
                n[k] = node["properties"][k][0]["value"]
        return n
    