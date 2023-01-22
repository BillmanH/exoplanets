import numpy as np
from numpy import random as r


def rnd(n, s,min_val=1):
    """
    returns positive int, within normal distribution
    n = mean, s = std
    """
    y = int(abs(np.ceil(r.normal(n, s))))
    if y < min_val:
        y=min_val
    return y

def rnd_dist(set):
    # Input should be a list of dicts, with a key annd percent 
    dist = []
    vals = []
    for i in set.keys():
        roll = np.random.normal(set[i]["mean"], set[i]["std"])
        if roll < 0:
            roll = 0
        vals.append(roll)
    vals = [np.round(t / np.sum(vals), 3) for t in vals]
    for j, k in enumerate(set.keys()):
        dist.append({k: vals[j]})
    return dist


def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])
