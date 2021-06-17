#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:38:15 2020

@author: admin
"""



import nltk

import gensim
from gensim import models
from gensim import corpora, similarities
from collections import defaultdict

from functions.Retrieve_Article_Content import retrieve_article_content
from functions.Pre_Process import preprocess
from functions.Progress_Bar import progress
from functions.Update_Topics_Table import update_topics_table

## pwd must be //theNewsroom/topic-modelling-analysis/topic_analysis ##

# Retrieve article content from thenewsroom database 
text_corpus = retrieve_article_content()


# Example text corpus for testing
# text_corpus = [
#     "Human machine interface for lab abc computer applications",
#     "A survey of user opinion of computer system response time",
#     "The EPS user interface management system",
#     "System and human system engineering testing of EPS",
#     "Relation of user perceived response time to error measurement",
#     "The generation of random binary unordered trees",
#     "The intersection graph of paths in trees",
#     "Graph minors IV Widths of trees and well quasi ordering",
#     "Graph minors A survey",
# ]

processed_articles = []

i = 0
for article in text_corpus:
    progress(i, len(text_corpus), 'Pre-processing article content')
    processed_articles.append(preprocess(article))
    i += 1


# Assign each word a unique ID
dictionary = corpora.Dictionary(processed_articles)

'''
Remove very rare and very common words:

- words appearing less than 15 times
- words appearing in more than 10% of all documents
'''
dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)


# Use the bag-of-words (bow) model to determine the frequency of each word
# and put words in the format (ID, frequency)
bow_corpus = [dictionary.doc2bow(text) for text in processed_articles]

print("\nRunning LDA topic analysis")
# LDA for multicore 
'''
Train your lda model using gensim.models.LdaMulticore and save it to 'lda_model'
'''
lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 10, 
                                   id2word = dictionary,                                    
                                   passes = 15,
                                   workers = 2)

lda_model.save('model5.gensim')
topics = lda_model.print_topics(num_words=10)

# Use this visualiser to help define the topics (it will open in your browser)

import pyLDAvis
import pyLDAvis.gensim as gensimvis
print('Pyldavis ....')
vis_data = gensimvis.prepare(lda_model, bow_corpus, dictionary)
pyLDAvis.show(vis_data)


# Test article on LDA model
test_article = text_corpus[0]
bow_vector = dictionary.doc2bow(preprocess(test_article))

test_result = lda_model[bow_vector]


update_topics_table()











