import numpy as np
import pickle, os
# I got the syllables by parsing out a global list of city names. 

syllables = pickle.load(open(os.path.join(os.getenv("ABS_PATH"),"app/creators/specs/syllables.p"), "rb"))

def make_word(n):
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()


def rnd(n, s):
    """
    returns positive int, within normal distribution
    n = mean, s = std
    """
    return int(abs(np.ceil(np.random.normal(n, s))))


def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])