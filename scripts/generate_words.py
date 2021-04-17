# %%

import pandas as pd

# %%
cities = pd.read_csv('../data/world-cities.csv')
cities['name'] = cities['name'].str.lower()
cities['country'] = cities['country'].str.lower()


ci = cities['name'].drop_duplicates().str.lower().values
co = cities['country'].drop_duplicates().str.lower().values


words = pd.concat([pd.DataFrame(ci),pd.DataFrame(co)]).drop_duplicates().values
words = " ".join(words.flatten())

# %%
from nltk.tokenize import SyllableTokenizer
from nltk import word_tokenize
SSP = SyllableTokenizer()

tokens = [SSP.tokenize(token) for token in word_tokenize(words)]


#%%
import numpy as np
syllables = np.unique(np.concatenate(tokens).ravel())
len(syllables)

#%%
pd.DataFrame(syllables).to_csv('../data/syllables.csv',encoding='utf-8')

def make_word(n):
    syl = np.random.choice(syllables,n)
    word = ''.join(syl)
    return word

make_word(3)