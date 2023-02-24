import pandas as pd
import numpy as np
import logging

def get_unique_consumption_values(x):
    y = [f"'{i.strip('][')}'" for i in x]
    y = ",".join(y)
    return y

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
    logging.info(f'{x.location_id} consumed {x.consumes}: {x.consumption}')
    c.run_query(query)

def tally_consumption(c,consumption_df,resources):
    for r in resources:
        resource = c.clean_node(r['objects'][1])
        location = c.clean_node(r['objects'][0])
        consumption_df.loc[consumption_df['location_id']==location['objid'],'available'] = resource['volume']
        consumption_df['remaining'] = consumption_df['available']-consumption_df['consumption']
        consumption_df['remaining'] = consumption_df['remaining'].fillna(-1)
    return consumption_df


def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])


def death_by_starvation_event(loc,pop,params):
    node = {
        'objdid':uuid,
        'name':'starvation',
        'label':'event',
        'text': f"The population ({pop['name'][0]}) enhabiting {loc['name'][0]} has died of starvation.",
        'visibleTo':pop['username'][0],
        'time':params['time']['currentTime'] 
    }
    return node

def delete_dead_pops(c,dead_pop_ids):
    ids = ",".join([f"'{i}'"  for i in dead_pop_ids])
    query = f"""
    g.V().has('objid',within({ids})).drop()
    """

    c.run_query(query)


def lower_health(c,x,params):
    dead_pop_nodes = []
    dead_pop_ids = []
    query =f"""
    g.V().has('objid','{x.location_id}').as('location').in('enhabits')
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
        consumes = i['objects'][2]['consumes']
        if x.consumes in consumes:
            if health <=0:
                dead_pop_nodes.append(death_by_starvation_event(i['objects'][0],i['objects'][1],params))
                dead_pop_ids.append(objid)
                if len(dead_pop_ids) > 30:
                    print(f"cache threshold of n pops reached. Purging {len(dead_pop_ids)}")
                    delete_dead_pops(c, dead_pop_ids)
                    c.upload_data({"nodes":dead_pop_nodes,"edges":[]})
                    dead_pop_ids = []
                    dead_pop_nodes = []
                    print('.',end="")
            else:
                starve_query = f"""
                g.V().has('objid','{objid}').property('health',{health-params['starve_damage']})
                """
                c.add_query(starve_query)
            # print(f"pop: {i['objects'][1]['objid'][0]},{i['objects'][1]['name'][0]} has run out of food and will suffer {health}-> {params['starve_damage']} ")
    print(f"Remaining pops purged due to starvation: {len(dead_pop_ids)}")
    if len(dead_pop_ids)>0:
        delete_dead_pops(c, dead_pop_ids)
        c.upload_data({"nodes":dead_pop_nodes,"edges":[]})
    print(f"{len(c.stack)} items in query stack")
    c.run_queries()


# this is the 'main' function:       
def consume(c,locations_df,species_df,params):
    # get the origional list of populations who would consume resources
    consumption_df = get_consumption_df(locations_df,species_df,params)
    # Some species consume more than one resource, so we extend
    consumption_df = expand_consumption_df(consumption_df)
    # Get the available resources for those locations
    c.run_query(make_resource_query(consumption_df))
    resources = c.res
    # Tally the consumption to get the remaining resources
    consumption_df = tally_consumption(consumption_df,resources)
    # for resources > 0 (have enough to eat), update those resources
    consumption_df[consumption_df['remaining']>0].apply(lambda x: make_resource_update_query(c,x),axis=1)
    # for locations with resources < 0 we lower the health of all populations
    consumption_df[consumption_df['remaining']<=0].apply(lambda x: lower_health(c,params,x),axis=1)