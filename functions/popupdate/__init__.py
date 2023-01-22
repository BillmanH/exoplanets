import datetime
import logging
import yaml

import azure.functions as func
from .db_functions import get_client, run_query, clean_node
from .time_functions import global_ticker


logger = logging.getLogger('azure.mgmt.resource')

params = yaml.safe_load(open('settings.yaml'))


def main(mytimer: func.TimerRequest) -> None:
    c = get_client()
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    

    healthy_pops_query = f"g.V().has('label','pop').has('health',gt({params['pop_health_requirement']}))"
    res = run_query(healthy_pops_query)


    ### END 
    logging.info(f'Population update trigger ran at: {utc_timestamp}')
    c.close()
