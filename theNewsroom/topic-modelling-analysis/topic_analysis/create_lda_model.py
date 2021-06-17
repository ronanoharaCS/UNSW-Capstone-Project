#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:38:15 2020

@author: admin
"""

import gensim
from gensim.models import LdaMulticore
from gensim import corpora, similarities
from collections import defaultdict
import pickle
import os
import pyLDAvis
import pyLDAvis.gensim as gensimvis

# User-Defined Funtions
from functions.Retrieve_Article_Content import retrieve_article_content
from functions.Pre_Process import preprocess
from functions.Progress_Bar import progress

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

## pwd must be //theNewsroom/topic-modelling-analysis/topic_analysis ##

user_defined_num_topics = int(input("How many topics is this for (e.g. '32')?\n"))

# Retrieve article content from thenewsroom database 
text_corpus = retrieve_article_content()

processed_articles = []

i = 0
for article in text_corpus:
    progress(i, len(text_corpus), 'Pre-processing article content')
    processed_articles.append(preprocess(article))
    i += 1

# Assign each word a unique ID
dictionary = corpora.Dictionary(processed_articles)

# Remove very rare and very common words:
# - words appearing less than 15 times
# - words appearing in more than 10% of all documents

dictionary.filter_extremes(no_below=15, no_above=0.10, keep_n= 100000)

# Use the bag-of-words (bow) model to determine the frequency of each word
# and put words in the format (ID, frequency)
bow_corpus = [dictionary.doc2bow(text) for text in processed_articles]


print("\nRunning LDA topic analysis for " + str(user_defined_num_topics) + ' topics')

# LDA for multicore 
lda_model =  LdaMulticore(bow_corpus, 
                                   num_topics = user_defined_num_topics, 
                                   id2word = dictionary,                                    
                                   passes = 15,
                                   workers = 3)


print("""\n\nUse this tool to assess the validity of the topic model.\n 
      It will load in your browser.\n
      Once finished, hit ctrl+C and then save or discard the model\n\n""")

# Use this visualiser to help define the topics (it will open in your browser)

print('Pyldavis ....')
vis_data = gensimvis.prepare(lda_model, bow_corpus, dictionary, sort_topics=False)
pyLDAvis.show(vis_data)

# Save the LDA Model and associated dictionary

lda_model_path = 'lda_models/' + str(user_defined_num_topics) + '_topics/gensim_lda_model'
dictionary_path = 'lda_dictionary/' + str(user_defined_num_topics) + '_topics/dict.pickle'

question = "Are you sure you want to overwrite the existing LDA model for " + str(user_defined_num_topics) + " topics? ('yes' or 'no')\n"
if os.path.exists(lda_model_path):
    response = input(question)
    
    if response in ('yes', 'Yes', ' yes', 'yes ', 'YES', 'yes.'):
        
        lda_model.save(lda_model_path, pickle_protocol = 2) # Save LDA model
        
        pickle_out = open(dictionary_path, "wb") # Save the dictionary
        pickle.dump(dictionary, pickle_out)
        pickle_out.close()
        print("LDA model saved") 
        
    else:
        print("LDA model not saved")

# If first time running this num_topics, need to create directories first
else:
    os.mkdir('lda_models/' + str(user_defined_num_topics) + '_topics/')
    lda_model.save(lda_model_path, pickle_protocol = 2)

    os.mkdir('lda_dictionary/' + str(user_defined_num_topics) + '_topics/')
    pickle_out = open(dictionary_path, "wb")
    pickle.dump(dictionary, pickle_out)
    pickle_out.close()
    print("LDA model saved")    












