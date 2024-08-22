
def getOrbitingBodies(c):
    response = {}
    objid = c.form['objid']
    label = c.form['type']
    c.run_query(f"g.V().has('objid','{objid}').in('{label}').valueMap()")
    children = c.clean_nodes(c.res)
    response['children'] = children
    return response


def getPopulations(c):
    response = {}
    objid = c.form['objid']
    label = c.form['type']
    c.run_query(f"g.V().has('objid','{objid}').in('isIn').valueMap()")
    children = c.clean_nodes(c.res)
    response['children'] = children
    return response


def getPopActions(c):
    response = {}
    objid = c.form['objid']
    label = c.form['type']
    c.run_query(f"g.V().has('objid','{objid}').in('{label}').valueMap()")
    children = c.clean_nodes(c.res)
    response['children'] = children
    return response
