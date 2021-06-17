#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:42:38 2020

@author: admin
"""

'''
Function's to perform the pre processing steps on the entire dataset
'''

import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

from collections import defaultdict

# Add stopwords to those provided by gensim.STOPWORDS, here
all_stop_words = STOPWORDS.union(set(["say","like","think","time","go","thing","know"])) # THIS ISN'T WORKING?


def lemmatize_stemming(text):
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))



# 1. Words that have fewer than 3 characters are removed.
# 2. All stopwords (redundant words. For example "and", "is", "are", "the") are removed.
# 3. Words are lemmatized — words in third person are changed to first person and verbs in past and future tenses are changed into present.
# 4. Words are stemmed — words are reduced to their root form.

def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text):
        if token not in all_stop_words and len(token) > 3: 
            result.append(lemmatize_stemming(token))
    
    return result




