import numpy as np
from numpy import random as r


def rnd(n, s):
    """
    returns positive int, within normal distribution
    n = mean, s = std
    """
    return int(abs(np.ceil(r.normal(n, s))))