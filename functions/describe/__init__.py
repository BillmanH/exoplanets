import datetime
import logging
import pandas as pd

import azure.functions as func
from .cmdb_graph import CosmosdbClient

logger = logging.getLogger('azure.mgmt.resource')


def main(mytimer: func.TimerRequest) -> None:
    c = CosmosdbClient()
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    


    logging.info(f'Python timer trigger function ran at: {utc_timestamp}')

# Example action query:
# 6816154304433