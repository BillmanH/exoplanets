import pickle
import numpy as np
import os
import logging

print("Loading syllables from: " + os.getcwd())

# note that languages should get this file from the same location in the az function. This will be different for the app
syllables = pickle.load(open(os.path.join("app","functions","syllables.p"), "rb"))
syllables_dist = pickle.load(open(os.path.join("app","functions","syllables_dist.p"), "rb"))

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