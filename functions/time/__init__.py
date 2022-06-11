import datetime
import logging

import azure.functions as func
from .db_functions import get_client, run_query, clean_node

logger = logging.getLogger('azure.mgmt.resource')
c = get_client()

print(f"Logger enabled for ERROR={logger.isEnabledFor(logging.ERROR)}, " \
    f"WARNING={logger.isEnabledFor(logging.WARNING)}, " \
    f"INFO={logger.isEnabledFor(logging.INFO)}, " \
    f"DEBUG={logger.isEnabledFor(logging.DEBUG)}")

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    # Get the current time node
    res = run_query(c,"g.V().hasLabel('time').valueMap()")
    time = [clean_node(n) for n in res][0]

    # Autoincrement time by one:
    currentTime = time['currentTime'] + 1
    print(f"time was discovered at:")
    print(time)
    updateRes = run_query(c, f"g.V().hasLabel('time').property('currentTime', {currentTime})")

    print(f"currentTime was updated to:{currentTime}")
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
