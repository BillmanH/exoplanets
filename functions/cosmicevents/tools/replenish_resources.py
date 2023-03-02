import logging


def get_replenishing_resources(c):
    renewables_query = f"""
    g.V().has('label','resource')
            .has('replenish_rate',gt(0)).valuemap()
    """
    c.run_query(renewables_query)
    data = c.clean_nodes(c.res)
    return data

def update_replenishing_resources(r):
        replenish_query = f"""
                g.V().has('objid','{r['objid']}').property('volume',{r['volume']+r['replenish_rate']})
        """
        return replenish_query


def renew_resources(c):
    data = get_replenishing_resources(c)
    logging.info(f"Total resources with the ability to renew: {len(data)}")
    if len(data)>0:
        for r in data:
            c.add_query(update_replenishing_resources(r))
        c.run_queries()
        logging.info(f'**** resources have been renewed ****')
    else:
        logging.info(f'**** No resources to renew ****')