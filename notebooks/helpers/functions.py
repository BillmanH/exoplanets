from numpy import random
import pickle, os
# I got the syllables by parsing out a global list of city names. 

syllables = pickle.load(open(os.path.join(os.getenv("abspath"),"app/creators/specs/syllables.p"), "rb"))

def make_word(n):
    syl = random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()