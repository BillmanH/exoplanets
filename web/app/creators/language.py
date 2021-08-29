import pickle
import numpy as np



syllables = pickle.load(open("web/app/creators/specs/syllables.p", "rb"))


def make_word(n, spaces=True):
    # TODO: Spaces not implemented
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()