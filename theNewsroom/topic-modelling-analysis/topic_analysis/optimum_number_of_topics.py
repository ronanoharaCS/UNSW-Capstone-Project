#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:29:38 2020

@author: admin
"""

from gensim.models.coherencemodel import CoherenceModel
from gensim import corpora
from gensim.models import LdaMulticore
import matplotlib.pyplot as plt

# User-Defined Functions
from functions.Retrieve_Article_Content import retrieve_article_content
from functions.Pre_Process import preprocess
from functions.Progress_Bar import progress


print("User input the range of the number of topics \n (E.g. start = 10, limit = 30, step = 5)")

start = int(input ("start:"))
limit = int(input ("limit:"))
step = int(input ("step:"))

if limit - start > 10 and step < 5:
    print("This may take a while..")

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

dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)


# Use the bag-of-words (bow) model to determine the frequency of each word
# and put words in the format (ID, frequency)
bow_corpus = [dictionary.doc2bow(text) for text in processed_articles]

coherence_values = []
model_list = []
print("\n\nCalculating coherence for:")
for num_topics in range(start, limit, step):
    print(str(num_topics) + ' topics')
    model =  LdaMulticore(bow_corpus, num_topics = num_topics, id2word = dictionary, passes = 15, workers = 3)
    model_list.append(model)
    coherencemodel = CoherenceModel(model=model, dictionary=dictionary, corpus = bow_corpus, coherence='u_mass')
    coherence_values.append(coherencemodel.get_coherence())

# Create a plot of coherence results
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')

# Save plot
image_path = 'coherence_results/start_' + str(start) + '_limit_' + str(limit) + '_step_' + str(step)
plt.savefig(image_path) 
print("RESULTS PLOT SAVED")

plt.close()





