import pandas as pd
import numpy as np
import logging
import yaml

from functools import reduce
import operator

# static queries that don't require variables
count_of_consumed_query = f"""
g.E()
    .has('label','inhabits').outV()
    .out('inhabits').dedup().values('name','label','objid')
"""

# count_of_consumed = f"""
# g.V().has('objid','{resourceId}').as('resource')
#     .in('has').out('inhabits').as('planet').groupcount().by('name').as('planet').path()
# """

def get_planets_consumption(c,planetId):
    count_of_consumed = f"""
    g.V().has('objid','{planetId}').as('planet')
        .in('inhabits').out('isOf').as('species').groupcount().by('consumes').as('consumes').path()
    """
    c.run_query(count_of_consumed)
    return reduce(operator.concat, [i['objects'] for i in c.res])

def get_consuming_planets(c):
    c.run_query(count_of_consumed_query)
    planets_that_have_pops = c.split_list_to_dict(c.res, ['name','label','objid'])
    # for each planet, get the consumption
    for iter,item in enumerate(planets_that_have_pops):
        planets_that_have_pops[iter]['consumes'] = get_planets_consumption(c,planets_that_have_pops[iter]['objid'])
    return planets_that_have_pops

def calculate_consumption(c,t):
    messages = []
    consuming_planets = get_consuming_planets(c)
    for planet in consuming_planets:
        messages.append(get_consumption_message(planet))
    return messages


def get_consumption_message(planet):
    message = {"agent":planet,"action":"consume"}
    return message



def reduce_location_resource(c,message, consumption):
    # find out if the location has the resource
    objid = message['agent']['objid']
    consuming = list(consumption.keys())[0]
    quantity = list(consumption.values())[0]
    resource_query = f"""
    g.V().has('objid','{objid}').out('has').has('label','resource').has('name','{consuming}').valuemap()
    """
    c.run_query(resource_query)
    if len(c.res) != 1:
        logging.info(f"EXOADMIN: {objid} has a resource issue - c.res:{c.res}")
    resource = c.clean_nodes(c.res)[0]
    if resource['volume'] > quantity:
        new_volume = resource['volume'] - quantity
        patch_resource_query = f"""
        g.V().has('objid','{objid}').out('has').has('label','resource').has('name','{consuming}')
            .property('volume', {new_volume})
        """
        c.run_query(patch_resource_query)
        logging.info(f"EXOADMIN: resources on {message['agent']['name']} reduced by {quantity}, {resource['volume']}-> {new_volume}")
    if resource['volume'] <= quantity:
        new_volume = 0
        patch_resource_query = f"""
        g.V().has('objid','{objid}').out('has').has('label','resource').has('name','{consuming}')
            .property('volume', {new_volume})
        """
        c.run_query(patch_resource_query)
        logging.info(f"EXOADMIN: resources on {message['agent']['name']} reduced by {quantity}, People at this location will starve.")
        starving_messages = get_starving_populations(c,message['agent'])
    return starving_messages


def get_starving_populations(c, agent, Action):
    starving_action = {
    "type": "starve",
    "label": "action",
    "applies_to": "pop",
    "effort": 0,
    "augments_self_properties": {"health": -7},
    "comment": "Populations that don't have enough resources will loose health until it reachees zero"
    }
    starving_job = {
        'created_at':t.params['currentTime'],
        'objid':f"starving_async_{t.params['currentTime']}",
    }
    location = agent['objid']
    starving_pop_query =f"""
    g.V().has('objid','{location}').in('inhabits').valuemap()
    """
    c.run_query(starving_pop_query)
    starving_pops = c.clean_nodes(c.res)
    starving_messages = []
    for pop in starving_pops:
        starving_action_message = {"agent":pop,"action":starving_action,"job":starving_job}
        starving_messages.append(starving_action_message)
    return starving_messages



def death_by_starvation_event(loc,pop,params):
    node = {
        'objid':uuid(),
        'name':'starvation',
        'label':'event',
        'text': f"The population ({pop['name'][0]}) inhabiting {loc['name']} has died of starvation.",
        'visibleTo':pop['username'][0],
        'time':params['currentTime'],
        'username':'azfunction'
    }
    return node

