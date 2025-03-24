import pandas as pd
import numpy as np
import logging
import yaml

from functools import reduce
import operator


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
 

def check_faction_has_resource(c,t,message):
    objid = message['agent']['objid']
    consuming = message['agent']['consumes'][0]
    faction_resource_query = f"""
    g.V().has('objid','{objid}').out('isIn').out('has').has('objtype','resource').has('type','{consuming}').valueMap()
    """
    logging.info(f"EXOADMIN: check_faction_has_resource query: {faction_resource_query}")
    c.run_query(faction_resource_query)
    if len(c.res) == 0:
        logging.info(f"EXOADMIN: faction: {objid} does not have the resource: {consuming}.")
        return False, None
    else:
        logging.info(f"EXOADMIN: {objid} has the resource - c.res:{c.res}")
        return True, c.clean_nodes(c.res)[0]

def reduce_faction_resources(c,t,message, consuming):
    """
    the message should contain the incoming pop (objid) and the resources that it consumes.
    query here will get the resources at the location the pop `inhabits`
    """
    # find out if the location has the resource
    logging.info(f"EXOADMIN: Processing reduce_faction_resources for: {message['agent']}")

    objid = message['agent']['objid']
    quantity = t.pop_growth_params['pop_consumes']
    logging.info(f"EXOADMIN: objid:{objid} consumes  {quantity} {consuming}")

    faction_resource_query = f"""
    g.V().has('objid','{objid}').out('isIn').out('has').has('objtype','resource').has('type','{consuming}').valuemap()
    """
    logging.info(f"EXOADMIN: faction_resource_query query: {faction_resource_query}")
    c.run_query(faction_resource_query)

    if len(c.res) != 1:
        logging.info(f"EXOADMIN: {objid} was not able to locate the resource - c.res:{c.res}")
    resource = c.clean_nodes(c.res)[0]
    old_volume = float(resource['volume'])
    new_volume = old_volume
    if float(resource['volume']) > quantity:
        new_volume = float(resource['volume']) - quantity
        logging.info(f"EXOADMIN: resources {resource['objid']} consumed by {message['agent']['objid']}: reduced by {quantity}, {resource['volume']}-> {new_volume}")
        patch_resource_query = f"g.V().has('objid','{resource['objid']}').property('volume',{new_volume})"
        c.run_query(patch_resource_query)
        logging.info(f"EXOADMIN: patch_resource_query: {patch_resource_query}")
    if float(resource['volume']) <= quantity:
        logging.info(f"EXOADMIN: location resources({resource['objid']}) is reduced to zero. {message['agent']['objid']} will starve.")
        starve_population(c,t,message)
        drop_resource_query = f"g.V().has('objid','{resource['objid']}').drop()"
        c.run_query(drop_resource_query)
        logging.info(f"EXOADMIN: resource {resource['objid']} has been dropped.")

def reduce_location_resource(c,t,message, consuming):
    """
    the message should contain the incoming pop (objid) and the resources that it consumes.
    query here will get the resources at the location the pop `inhabits`
    """
    # find out if the location has the resource
    logging.info(f"EXOADMIN: Processing reduce_location_resource for: {message['agent']}")
    objid = message['agent']['objid']
    quantity = t.pop_growth_params['pop_consumes']
    logging.info(f"EXOADMIN: objid:{objid} consumes  {quantity} {consuming}")

    location_resource_query = f"""
    g.V().has('objid','{objid}').out('inhabits').out('has').has('objtype','resource').has('type','{consuming}').valuemap()
    """
    logging.info(f"EXOADMIN: location_resource_query query: {location_resource_query}")
    c.run_query(location_resource_query)

    if len(c.res) == 0:
        logging.info(f"EXOADMIN: {objid} was not able to locate the resource {consuming}")
    else:
        resource = c.clean_nodes(c.res)[0]
        old_volume = float(resource['volume'])
        new_volume = old_volume
    
        if float(resource['volume']) > quantity:
            new_volume = float(resource['volume']) - quantity
            logging.info(f"EXOADMIN: resources {resource['objid']} consumed by {message['agent']['objid']}: reduced by {quantity}, {resource['volume']}-> {new_volume}")
        if float(resource['volume']) <= quantity:
            new_volume = 0
            logging.info(f"EXOADMIN: location resources({resource['objid']}) is reduced to {new_volume}. {message['agent']['objid']} will starve.")
            starve_population(c,t,message)
    patch_resource_query = f"g.V().has('objid','{resource['objid']}').property('volume',{new_volume})"
    logging.info(f"EXOADMIN: patch_resource_query: {patch_resource_query}")
    c.run_query(patch_resource_query)
    logging.info(f"EXOADMIN: agent: {objid} consumed resource: {resource['objid']}. {old_volume}->{new_volume}")

def consume(c,t,message, consuming):
    # check that the faction has the resouce to consume
    faction_has_resource, faction_resource = check_faction_has_resource(c,t,message)
    if faction_has_resource:
        # reduce the resource at the location
        logging.info(f"EXOADMIN: faction has the resource: {faction_resource}")
        reduce_faction_resources(c,t,message, consuming)
    else:
        # reduce the resource at the location
        logging.info(f"EXOADMIN: faction does not have the resource. Local reasources will be consumed.")
        reduce_location_resource(c,t,message, consuming)



def starve_population(c, t, message):
    starve_value = 0.05
    popid = message['agent']['objid']
    logging.info(f"EXOADMIN: starve_population for {popid}: {starve_value}")
    starved_pop = c.delta_property(popid,'health',.05)
    if starved_pop['health'] < 0:
        pop_dies(c,t,message['agent'])


def pop_dies(c,t,pop):
    c.run_query(f"g.V().has('objid','{pop['objid']}').drop()")
    logging.info(f"EXOADMIN: {pop['name']}:{pop['objid']} has died of starvation.")


