import datetime
import logging

import azure.functions as func
from .db_functions import get_client, run_query, clean_node
from .time_functions import global_ticker

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

    ### Start of time_funtions here
    global_ticker(c,time)


    ### End of time_functions



    logging.info(f'Python timer trigger function ran at: {utc_timestamp}')
    c.close()

