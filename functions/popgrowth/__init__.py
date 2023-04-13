import datetime
import logging
import yaml, pickle
import pandas as pd
import numpy as np

import azure.functions as func
from .cmdb_graph import CosmosdbClient
from .tools import consumption, growth
import os

logger = logging.getLogger('azure.mgmt.resource')



try:
    params = yaml.safe_load(open('settings.yml'))
    syllables = pickle.load(open('syllables.p', "rb"))
except:
    params = yaml.safe_load(open('popgrowth/settings.yml'))
    syllables = pickle.load(open('popgrowth/syllables.p', "rb"))



def main(mytimer: func.TimerRequest) -> None:
    c = CosmosdbClient()
    logging.info(f'CDB endpoint: {c.endpoint}')
    logging.info(f"[param] amount people will suffer by starving: {params['starve_damage']}")
    logging.info(f"[param] amount of health needed to grow: {params['pop_health_requirement']}")
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    c.run_query("g.V().hasLabel('time').valueMap()")
    params['time'] = c.clean_nodes(c.res)[0]

    consumption.consume(c,params)
    growth.grow(c,params,syllables)

    ### END 
    logging.info(f'Population Growth trigger ran at: {utc_timestamp}')

