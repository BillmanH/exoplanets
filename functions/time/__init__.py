import datetime
import logging
import pandas as pd

import azure.functions as func
from .connectors.cmdb_graph import CosmosdbClient

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

    if mytimer.past_due:
        logging.info('The timer is past due!')

    ### START of time_funtions here
    
    # not to be confused with python's time object in the datetime library
    time = time.Time(c)
    time.get_current_UTU()
    logging.info(time)
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
            action_event = make_action_event(c,agent,job,params)
            action_edge = c.create_custom_edge(action_event,agent,'completed')
            c.add_query(c.create_vertex(action_event,'event'))
            c.add_query(action_edge)
            # print(c.stack)
            logging.info(f'validActionCounter: {validActionCounter}, total queries:{len(c.stack)}')
            c.run_queries()

            

    logging.info(f'Total ations resolved in this run: {validActionCounter}')
    
    # Increment global time
    time.global_ticker()
    
    ### END of time_functions


    logging.info(f'Python timer trigger function ran at: {utc_timestamp}')
