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


def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])
