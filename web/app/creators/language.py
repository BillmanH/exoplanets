import pickle
import numpy as np
import yaml


try:
    syllables = pickle.load(open("../data/syllables.p", "rb"))
except FileNotFoundError:
    syllables = pickle.load(open("data/syllables.p", "rb"))


pdata = yaml.safe_load(open('web/app/creators/specs/planet.yaml'))["planet_types"]
mdata = yaml.safe_load(open('web/app/creators/specs/moon.yaml'))["moon_types"]


def make_word(n, spaces=True):
    # TODO: Spaces not implemented
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()