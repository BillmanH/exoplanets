import numpy as np
import pandas as pd



def get_pops(c,userguid):
    query = f"""
    g.V().hasLabel('pop').has('userguid','{userguid}').valuemap()
    """
    c.run_query(query)
    df = pd.DataFrame(c.clean_nodes(c.res))
    return df

def get_random_pop(c,userguid):
    df = get_pops(c,userguid)
    pop = df.sample(1).reset_index(drop=True).T.to_dict()[0]
    return pop