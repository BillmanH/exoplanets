import pickle
import numpy as np
from numpy import random as r

syllables = pickle.load(open("../data/syllables.p", "rb"))

#%%
def make_word(n):
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word


def rnd(n, s):
    """
    returns positive int, within normal distribution
    n = mean, s = std
    """
    return int(abs(np.ceil(r.normal(n, s))))


def uuid(n=8):
    return "".join([str(i) for i in np.random.choice(range(10), n)])


def build_homeSystem(data):

    return data