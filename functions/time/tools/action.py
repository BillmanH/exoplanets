import logging
import yaml
import numpy as np

def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])

def make_action_event(c,pop,act,params):
    node = {
        'objid': f"{uuid()}",
        'name':'job',
        'label':'event',
        'text': f"The population ({pop['name']}) has completed {act['actionType']}",
        'visibleTo':pop['username'],
        'time':params['currentTime'],
        'username':'event'
    }
    return node

def validate_action_time(time,a):
    '''
    validate that the time to complete the task has passed. 
    Not the same as validation that the action can be taken. 
    If the `takingAction` edge has been applied to the agent `a`, then it is just a check of time completed. 
    '''
    if int(a['weight']) < int(time['currentTime']):
        return True
    else:
        return False

def get_global_actions(c):
    """
    Retrieve a list of the global actions.
    """
    # Autoincrement time by one:
    actions_query = """
        g.V().haslabel('action').as('action')
                    .inE('takingAction').has('status','pending').as('job')
                    .outV().as('agent')
                    .select('action','job','agent')
    """

    c.run_query(actions_query)
    actions = c.res
    return actions

def mark_action_as_resolved(c,agent, job):
    patch_job = f"""
    g.V().has('objid','{agent['objid']}')
            .outE('takingAction')
            .has('actionType', '{job['actionType']}')
            .has('weight','{job['weight']}')
            .property('status', 'resolved')
    """    
    logging.info(f"updating job: {job['actionType']}:{job['weight']}")
    c.add_query(patch_job)

def mark_agent_idle(c, agent):
    if 'isIdle' in agent.keys():
        idleQuery = f"""
        g.V().has('objid','{agent['objid']}').property('isIdle','true')
        """
        c.add_query(idleQuery)

def parse_properties(node):
    n = {}
    for k in node["properties"].keys():
        if len(node["properties"][k]) == 1:
            n[k] = node["properties"][k][0]["value"]
    return n

def resolve_augments_self_properties(agent, action):
    agent = agent.copy()
    self_properties = yaml.safe_load(action["augments_self_properties"])
    for p in self_properties.keys():
        agent[p] = agent[p] + float(self_properties[p])
    return agent

def query_patch_properties(agent, action):
    query = f"g.V().has('objid','{agent['objid']}')"
    for n in yaml.safe_load(action["augments_self_properties"]):
        query += f".property('{n}',{agent[n]})"
    return query

def resolve_action(c,agent,action):
    if "augments_self_properties" in action.keys():
        agent = resolve_augments_self_properties(agent, action)
        property_patch = query_patch_properties(agent, action)
        c.run_query(property_patch)

    

