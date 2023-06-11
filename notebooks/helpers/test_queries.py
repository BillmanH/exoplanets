import numpy as np
import pandas as pd



def get_pops(c,username):
    query = f"""
    g.V().hasLabel('pop').has('username','{username}').valuemap()
    """
    c.run_query(query)
    df = pd.DataFrame(c.clean_nodes(c.res))
    return df

def get_random_pop(c,username):
    df = get_pops(c,username)
    pop = df.sample(1).reset_index(drop=True).T.to_dict()[0]
    return pop