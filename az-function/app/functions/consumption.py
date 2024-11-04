import pandas as pd
import numpy as np
import logging
import yaml

from functools import reduce
import operator

# # static queries that don't require variables
# count_of_consumed_query = f"""
# g.E()
#     .has('label','inhabits').outV()
#     .out('inhabits').dedup().values('name','label','objid')
# """

# count_of_consumed = f"""
# g.V().has('objid','{resourceId}').as('resource')
#     .in('has').out('inhabits').as('planet').groupcount().by('name').as('planet').path()
# """

# def get_planets_consumption(c,planetId):
#     count_of_consumed = f"""
#     g.V().has('objid','{planetId}').as('planet')
#         .in('inhabits').out('isOf').as('species').groupcount().by('consumes').as('consumes').path()
#     """
#     c.run_query(count_of_consumed)
#     return reduce(operator.concat, [i['objects'] for i in c.res])



def get_consuming_pops(c):
    consuming_pops_query = "g.V().hasLabel('pop').as('pop').out('isOf').as('species').path().by('objid').by(values('consumes','effuses').fold())"
    c.run_query(consuming_pops_query)
    consuming_pops_res = [p['objects'] for p in c.res]
    consuming_pops = []
    for i in consuming_pops_res:
        a = {'objid': i[0], 'consumes': i[1][0].split(), 'effuses': i[1][1].split(',')}
        consuming_pops.append(a)
    return consuming_pops


def calculate_consumption(c,t):
    messages = []
    consuming_pops = get_consuming_pops(c)
    for r in consuming_pops:
        messages.append(get_consumption_message(r))
    return messages

def get_consumption_message(pop):
    message = {"agent":pop,"action":"consume"}
    return message
 

def consumption.reduce_location_or_faction_resource(c,t,message,resource):
    resource_query = f"""
    g.V().has('objid','{objid}').as('pop')
        .local(
            union(
                out('isIn').as('faction').out('has').has('objtype','resource').as('faction_resource'),
                out('inhabits').as('location').out('has').has('objtype','resource').as('location_resource'),
                )
                .fold()).as('faction_resource','location_resource')
                .path()
                .by(unfold().valueMap().fold())
    """
    c.run_query(resource_query)
    c.res

def reduce_location_resource(c,t,message, consuming):
    # find out if the location has the resource
    objid = message['agent']['objid']
    quantity = t.pop_growth_params['pop_consumes']

    if len(c.res) != 1:
        logging.info(f"EXOADMIN: {objid} was not able to locate the resource - c.res:{c.res}")
    resource = c.clean_nodes(c.res)[0]
    starving_messages = []
    if float(resource['volume']) > quantity:
        logging.info(f"EXOADMIN: resources on {message['agent']['name']}:{message['agent']['objid']} reduced by {quantity}, {resource['volume']}-> {new_volume}")
        new_volume = float(resource['volume']) - quantity
    if float(resource['volume']) <= quantity:
        logging.info(f"EXOADMIN: resources on {message['agent']['name']}:{message['agent']['objid']} reduced by {quantity}, People at this location will starve.")
        new_volume = 0
        starving_messages = get_starving_population_messages(c,t,message['agent'])
    patch_resource_query = f"""
    g.V().has('objid','{objid}').out('has').has('label','resource').has('name','{consuming}')
        .property('volume', {new_volume})
    """
    c.run_query(patch_resource_query)
    return starving_messages


def get_starving_population_messages(c, t, agent):
    starving_action = {
    "type": "starve",
    "label": "action",
    "applies_to": "pop",
    "effort": 0,
    "augments_self_properties": {"health": t.pop_growth_params['starve_damage']},
    "comment": "Populations that don't have enough resources will loose health until it reachees zero"
    }
    starving_job = {
        'created_at':t.params['currentTime'],
        'objid':f"starving_async_{t.params['currentTime']}",
        'actionType':'automatic'
    }
    location = agent['objid']
    starving_pop_query =f"""
    g.V().has('objid','{location}').in('inhabits').valuemap()
    """
    c.run_query(starving_pop_query)
    starving_pops = c.clean_nodes(c.res)
    starving_messages = []
    for pop in starving_pops:
            if float(pop.get('health',0)) > 0:
                starving_action_message = {"agent":pop,"action":starving_action,"job":starving_job}
                starving_messages.append(starving_action_message)
            else:
                pop_dies(c,t,pop)
    logging.info(f"EXOADMIN: {len(starving_messages)} starving messages created for the inhabitants of: {agent['name']}:{agent['objid']}")
    return starving_messages

def pop_dies(c,t,pop):
    c.run_query(f"g.V().has('objid','{pop['objid']}').drop()")
    logging.info(f"EXOADMIN: {pop['name']}:{pop['objid']} has died of starvation.")
    return pop

