import datetime
import logging

import azure.functions as func
from .db_functions import get_client, run_query, clean_node
from .time_functions import global_ticker
from .action import get_global_actions, validate_action, augments_self_properties

logger = logging.getLogger('azure.mgmt.resource')


def main(mytimer: func.TimerRequest) -> None:
    c = get_client()
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    # Time is constant, pulled in once at the begining of the function
    res = run_query(c,"g.V().hasLabel('time').valueMap()")
    time = [clean_node(n) for n in res][0]

    ### START of time_funtions here

    # Get all pending actions
    actions = get_global_actions(c)

    # resolve each actionn 
    validActionCounter = 0
    for a in actions:
        if validate_action(time,a['job']):
            logging.info(f'Total ations resolved in this run: {validActionCounter}')
            validActionCounter += 1
            if 'augments_self_properties' in list(a['job'].keys()):
                patch = run_query(c, augments_self_properties(a['agent'],a['job']))
            # set the job to resolved
            res = run_query(c, f"g.V().has('objid','{a['agent']['objid']}').outE('takingAction').has('actionType', '{a['job']['actionType']}').has('status', 'pending').has('weight',{a['job']['weight']}).property('status', 'resolved')")
            # set the agent to isIdle=True
            if 'isIdle' in list(a['agent'].keys()):
                res = run_query(c, f"g.V().has('objid','{a['agent']['objid']}').property('isIdle','true')")

    logging.info(f'Total ations resolved in this run: {validActionCounter}')

    # Increment global time
    global_ticker(c,time)
    
    ### END of time_functions


    logging.info(f'Python timer trigger function ran at: {utc_timestamp}')
    c.close()

