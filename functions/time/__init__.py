import datetime
import logging
import pandas as pd

import azure.functions as func
from .cmdb_graph import CosmosdbClient

from .time_functions import global_ticker
from .tools.action import (get_global_actions, 
                        validate_action_time, 
                        parse_properties, 
                        resolve_action,
                        make_action_event,
                        mark_action_as_resolved,
                        mark_agent_idle)

logger = logging.getLogger('azure.mgmt.resource')


def main(mytimer: func.TimerRequest) -> None:
    c = CosmosdbClient()
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    # Time is constant, pulled in once at the begining of the function
    c.run_query("g.V().hasLabel('time').valueMap()")
    time = c.clean_nodes(c.res)[0]

    ### START of time_funtions here

    # Get all pending actions
    actions = get_global_actions(c)
    actions_df = pd.DataFrame(actions)
    
    logging.info(f'total jobs: {actions_df.shape[0]}')
    validActionCounter = 0
    for i in actions_df.index:
        agent = parse_properties(actions_df.loc[i].agent)
        action = parse_properties(actions_df.loc[i].action)
        job = actions_df.loc[i].job['properties']

        logging.info(f'job: {job}')
        if validate_action_time(time,job):
            validActionCounter += 1
            resolve_action(c,agent,action)
            mark_action_as_resolved(c,agent, job)
            mark_agent_idle(c, agent)
            action_event = make_action_event(c,agent,job)
            c.add_query(c.create_custom_edge(action_event,agent,'completed'))
            c.add_query(c.create_vertex(action_event))
            logging.info(f'validActionCounter: {validActionCounter}')
            

    logging.info(f'Total ations resolved in this run: {validActionCounter}')
    # Increment global time
    global_ticker(c,time)
    
    ### END of time_functions


    logging.info(f'Python timer trigger function ran at: {utc_timestamp}')
