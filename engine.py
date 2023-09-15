# Backend functions runnign on a separate server.
# The Engine is something that is running all of the time. 
# Manages the passage of time, and the resolution of actions.


import datetime
import logging
import pandas as pd
import yaml, pickle

from app.connectors.cmdb_graph import CosmosdbClient
from app.objects import time as t
from app.functions import consumption, growth, replenish_resources

logging.basicConfig(filename='engine.log', level=logging.INFO)


params = yaml.safe_load(open('app/configurations/popgrowthconfig.yaml'))
syllables = pickle.load(open('app/creators/specs/syllables.p', "rb"))



def time(c):
    # Increments time and resolves actions
    # not to be confused with python's time object in the datetime library
    time = t.Time(c)
    time.get_current_UTU()
    logging.info(f'*** Time function ran at: {time }')
    # Get all pending actions 
    time.get_global_actions()
    actions_df = pd.DataFrame(time.actions)
    
    logging.info(f'Total jobs: {actions_df.shape[0]}')
    validActionCounter = 0 
    for i in actions_df.index:
        action = t.Action(c,actions_df.loc[i])
        if action.validate_action_time(time):
            validActionCounter += 1
            action.add_updates_to_c(time)
            action.resolve_action()
            logging.info(f'{action} was resolved')

    logging.info(f'Total actions resolved in this run: {validActionCounter}')
    
    # Increment global time
    time.global_ticker()

    logging.info(f'*** Time function ended')

    return time



def popgrowth(c,t):
    logging.info(f'*** Population growth function started at: {t }')
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    params['currentTime'] = t.params['currentTime']

    consumption.consume(c,params)

    growth.grow(c,params)
    logging.info(f'*** Population growth ended')




def main():
    runtime = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'*** Engine started at: {runtime}')
    c = CosmosdbClient()
    t = time(c)
    popgrowth(c,t)
    replenish_resources.renew_resources(c)
    endtime = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'*** Engine finsihed at: {endtime}')

if __name__ == "__main__":
    main()