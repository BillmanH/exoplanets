import pandas as pd
import numpy as np
import logging
import yaml

def get_unique_consumption_values(x):
    y = [f"'{i.strip('][')}'" for i in x]
    y = ",".join(y)
    return y

def all_pops_consumption(c):
    healthy_pops_query = f"""
    g.V().has('label','pop').as('pop')
        .local(
            union(
                out('inhabits').as('location'),
                out('isOfSpecies').as('species')
                )
                .fold()).as('location','species')
            .path()
            .by(unfold().valueMap().fold())
    """
    c.run_query(healthy_pops_query)
    data = c.reduce_res(c.res)
    pops_df = pd.DataFrame([d['pop'] for d in data])
    species_df = pd.DataFrame([d['species'] for d in data])
    locations_df = pd.DataFrame([d['location'] for d in data])
    logging.info(f"A total of {len(pops_df)} are about to be processed for consumption")
    return(pops_df,species_df,locations_df)

def get_consumption_df(locations_df,species_df,params):
    consumption_df = pd.DataFrame(pd.concat([
            locations_df,species_df.drop('objid',axis=1)
        ],axis=1).groupby([
            'objid',
            'consumes'
            ]).count().iloc[:,1]).reset_index()

    consumption_df.columns = ['location_id','consumes','pop']
    consumption_df['consumption'] = consumption_df['pop'] * params['pop_consumes']
    logging.info(f"A total of {consumption_df['pop'].sum()} pops will consume {consumption_df['consumption'].sum()} resources")
    return consumption_df

def expand_consumption_df(consumption_df):
    consumption_df['multi'] = consumption_df['consumes'].apply(lambda x: '[' in x )

    multi_consumption = pd.DataFrame(columns=consumption_df.columns)

    for i in consumption_df[consumption_df['multi']].index:
        l = yaml.safe_load(consumption_df.loc[i,'consumes'])
        for j in l:
            ser = consumption_df.loc[i]
            ser.consumes = j
            multi_consumption.loc[i] = ser
    consumption_df = consumption_df[consumption_df['multi']==False]
    consumption_df = pd.concat([consumption_df,multi_consumption]).reset_index(drop=True)
    return consumption_df

def make_resource_query(consumption_df):
    withinstring = "','".join(consumption_df['location_id'].drop_duplicates().tolist())
    consumesstring = get_unique_consumption_values(consumption_df['consumes'].drop_duplicates().tolist())
    query = f"g.V().has('objid',within('{withinstring}')).as('location')"
    query += f".out('hasResource').has('name',within({consumesstring})).as('resource').path().by(valueMap('objid','name')).by(valueMap('volume','objid','name'))"
    logging.info(f'Resources to consume: {consumesstring}')
    return query

def make_resource_update_query(c,x):
    query = f"g.V().has('objid','{x.location_id}').out('hasResource').has('name','{x.consumes}').property('volume',{int(x.remaining)})"
    logging.info(f'{x.location_id} consumed {x.consumes}: {x.consumption}, remaining: {x.remaining}')
    c.run_query(query)

def tally_consumption(c,consumption_df,resources):
    for r in resources:
        resource = c.clean_node(r['objects'][1])
        location = c.clean_node(r['objects'][0])
        consumption_df.loc[consumption_df['location_id']==location['objid'],'available'] = int(resource['volume'])
    consumption_df['remaining'] = consumption_df['available']-consumption_df['consumption']
    consumption_df.loc[consumption_df['remaining']<0,'remaining'] = -1
    consumption_df['remaining'] = consumption_df['remaining'].fillna(-1)
    return consumption_df


def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])


def death_by_starvation_event(loc,pop,params):
    node = {
        'objid':uuid(),
        'name':'starvation',
        'label':'event',
        'text': f"The population ({pop['name'][0]}) inhabiting {loc['name']} has died of starvation.",
        'visibleTo':pop['username'][0],
        'time':params['time']['currentTime'],
        'username':'azfunction'
    }
    return node


def delete_dead_pops(c,dead_pop_ids):
    ids = ",".join([f"'{i}'"  for i in dead_pop_ids])
    query = f"""
    g.V().has('objid',within({ids})).drop()
    """

    c.run_query(query)


def lower_health(c,params,x):
    dead_pop_nodes = []
    dead_pop_ids = []
    death_event_edges = []
    query =f"""
    g.V().has('objid','{x.location_id}').as('location').in('inhabits')
        .haslabel('pop').as('pop')
        .out('isOfSpecies').as('species')
        .path()
            .by(valueMap('objid','name'))
            .by(valueMap('name','objid','health','username'))
            .by(valueMap('name','objid','consumes'))
    """
    c.run_query(query)
    out = c.res
    print(f"{len(out)} pops will starve in {x.location_id}")
    for i in out:
        health = i['objects'][1]['health'][0]
        objid = i['objects'][1]['objid'][0]
        consumes = yaml.safe_load(i['objects'][2]['consumes'][0])
        all_death = 0
        # logging.info(f'health: {x.consumes,consumes}')
        if x.consumes in consumes:
            if health <= 0:
                death_event = death_by_starvation_event(c.clean_node(i['objects'][0]),i['objects'][1],params)
                dead_pop_nodes.append(death_event)
                death_event_edges.append(c.create_custom_edge(death_event, c.clean_node(i['objects'][0]), 'happenedAt'))
                dead_pop_ids.append(objid)
                all_death+=1
                if len(dead_pop_ids) > 30:
                    print(f"cache threshold of n pops reached. Purging {len(dead_pop_ids)}")
                    delete_dead_pops(c, dead_pop_ids)
                    upload_data = {'nodes':dead_pop_nodes,'edges':[]}
                    c.upload_data(data=upload_data)
                    dead_pop_ids = []
                    dead_pop_nodes = []
                    death_event_edges = []
                    for e in death_event_edges:
                        c.add_query(e)
                    c.run_queries()
                    print('.',end="")
            else:
                # logging.info(f'starving: {health}')
                starve_query = f"""
                g.V().has('objid','{objid}').property('health',{health-params['starve_damage']})
                """
                c.add_query(starve_query)
            
    if len(dead_pop_ids)>0:
        delete_dead_pops(c, dead_pop_ids)
        upload_data = {'nodes':dead_pop_nodes,'edges':[]}
        c.upload_data(data=upload_data)
        for e in death_event_edges:
            c.add_query(e)
    # logging.info(f'stack: {len(c.stack)}')
    c.run_queries()
    logging.info(f'Total deaths due to starvation at {x.location_id}: {all_death}')


# this is the 'main' function:       
def consume(c,params):
    # query to get all pops
    pops_df,species_df,locations_df = all_pops_consumption(c)
    # get the origional list of populations who would consume resources
    consumption_df = get_consumption_df(locations_df,species_df,params)
    # Some species consume more than one resource, so we extend
    consumption_df = expand_consumption_df(consumption_df)
    # Get the available resources for those locations
    c.run_query(make_resource_query(consumption_df))
    resources = c.res
    # Tally the consumption to get the remaining resources
    consumption_df = tally_consumption(c,consumption_df,resources)
    # for resources > 0 (have enough to eat), update those resources
    consumption_df.apply(lambda x: make_resource_update_query(c,x),axis=1)
    # for locations with resources < 0 we lower the health of all populations
    consumption_df[consumption_df['remaining']<=0].apply(lambda x: lower_health(c,params,x),axis=1)
    print(consumption_df)