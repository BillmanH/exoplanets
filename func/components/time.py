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
        actions_query = """
            g.V().haslabel('action').as('action')
                        .inE('takingAction').has('status','pending').as('job')
                        .outV().as('agent')
                        .select('action','job','agent')
        """

        self.c.run_query(actions_query)
        self.actions = [self.c.parse_all_properties(i) for i in self.c.res]


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
