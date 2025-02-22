
def getOrbitingBodies(c):
    response = {}
    objid = c.form['objid']
    label = c.form['type']
    c.run_query(f"g.V().has('objid','{objid}').in('{label}').valueMap()")
    children = c.clean_nodes(c.res)
    response['children'] = children
    return response


def getFactionChildren(c):
    response = {}
    objid = c.form['objid']
    label = c.form['type']
    pops_query = f"g.V().has('objid','{objid}').in('isIn').valueMap()" 
    resources_query = f"g.V().has('objid','{objid}').out('has').valueMap()"
    c.add_query(pops_query)
    c.add_query(resources_query)
    c.run_queries()
    pops = c.clean_nodes(c.res[pops_query])
    resources = c.clean_nodes(c.res[resources_query])
    response['pops'] = pops
    response['resources'] = resources
    return response


def getPopActions(c):
    response = {}
    objid = c.form['objid']
    label = c.form['type']
    c.run_query(f"g.V().has('objid','{objid}').in('{label}').valueMap()")
    children = c.clean_nodes(c.res)
    response['children'] = children
    return response
