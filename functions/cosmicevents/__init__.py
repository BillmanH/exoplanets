import logging
import yaml, pickle
import pandas as pd
import numpy as np

import azure.functions as func
from .cmdb_graph import CosmosdbClient
from .tools import replenish_resources
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

    if mytimer.past_due:
        logging.info('The timer is past due!')

    replenish_resources.renew_resources(c)


    ### END 
    logging.info(f'Resource renewal completed')

