# %%

import pickle
import re

import numpy as np
import pandas as pd
from nltk import word_tokenize
from nltk.tokenize import SyllableTokenizer

# %%
cities = pd.read_csv("../data/world-cities.csv")
cities["name"] = cities["name"].str.lower()
cities["country"] = cities["country"].str.lower()


ci = cities["name"].drop_duplicates().str.lower().values
co = cities["country"].drop_duplicates().str.lower().values


words = pd.concat([pd.DataFrame(ci), pd.DataFrame(co)]).drop_duplicates().values
words = " ".join(words.flatten())


SSP = SyllableTokenizer()

tokens = [SSP.tokenize(token) for token in word_tokenize(words)]


#%%

syllables = np.unique(np.concatenate(tokens).ravel())
len(syllables)

#%%
pd.DataFrame(syllables).to_csv("../data/syllables.csv", encoding="utf-8")

#%%
pickle.dump(syllables, open("../data/syllables.p", "wb"))
syllables = pickle.load(open("../data/syllables.p", "rb"))


syl = [i for i in syllables if type(i)==str]
clean_syll = [i for i in syl if re.match("[a-z]+$",i)]
len(syllables),len(syl),len(clean_syll)

pickle.dump(clean_syll, open("../data/syllables.p", "wb"))
#%%
def make_word(n):
    syl = np.random.choice(clean_syll, n)
    word = "".join(syl)
    return word


[make_word(3) for word in range(10)]

