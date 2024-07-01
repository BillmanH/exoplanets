import pickle
import numpy as np
import os
import logging


# note that languages should get this file from the same location in the az function. This will be different for the app
try:
    syllables = pickle.load(open("/home/site/wwwroot/syllables.p", "rb"))
    syllables_dist = pickle.load(open("/home/site/wwwroot/syllables_dist.p", "rb"))
except:
    print('loading syllables from ', os.getcwd())
    syllables = pickle.load(open("syllables.p", "rb"))
    syllables_dist = pickle.load(open("syllables_dist.p", "rb"))

# See `notebooks/Naming Things.ipynb` for the logic

# Makes random words using syllables
def make_word(n):
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()

# Same as `make_word` but uses the distribution of the data `p` to prefer more common syllables
def make_dist_word(n):
    syl = np.random.choice(syllables, n, p=syllables_dist)
    word = "".join(syl)
    return word.capitalize()