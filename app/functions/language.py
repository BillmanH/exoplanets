import pickle
import numpy as np
import os

if os.getenv("abspath") is not None:
    syllables = pickle.load(open(os.path.join(os.getenv("abspath"),"app/creators/specs/syllables.p"), "rb"))
    syllables_dist = pickle.load(open(os.path.join(os.getenv("abspath"),"app/creators/specs/syllables_dist.p"), "rb"))
else:
    syllables = pickle.load(open("app/creators/specs/syllables.p", "rb"))
    syllables_dist = pickle.load(open("app/creators/specs/syllables_dist.p", "rb"))

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