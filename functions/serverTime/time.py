import datetime
import logging
import pandas as pd

from app.connectors.cmdb_graph import CosmosdbClient
from app.objects import time as t



def main():
    c = CosmosdbClient()

    ### START of time_funtions here
    
    # not to be confused with python's time object in the datetime library
    time = t.Time(c)
    time.get_current_UTU()
    logging.info(time)
    # Get all pending actions
    time.get_global_actions()
    actions_df = pd.DataFrame(time.actions)
    
    logging.info(f'total jobs: {actions_df.shape[0]}')
    validActionCounter = 0 
    for i in actions_df.index:
        action = t.Action(c,actions_df.loc[i])
        if action.validate_action_time(time):
            validActionCounter += 1
            action.add_updates_to_c(time)
            action.resolve_action()
            logging.info(f'{action} was resolved')


            

    logging.info(f'Total ations resolved in this run: {validActionCounter}')
    
    # Increment global time
    time.global_ticker()
    
    ### END of time_functions


    logging.info(f'Python timer trigger function ran at: {time }')
