#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 19:58:39 2020

@author: admin
"""

from functions.num_articles import thenewsroom_db_num_articles
from functions.connect_to_db import connect_to_thenewsroom_db
from functions.Pre_Process import preprocess
from functions.Progress_Bar import progress

from psycopg2 import Error
from gensim.models import LdaMulticore
from gensim import corpora
import pickle

num_topics = input ("How many topics does the LDA topic model have? \n(atm only '32' will work)\n:")

num_articles = thenewsroom_db_num_articles()

conn, cur = connect_to_thenewsroom_db(1000) # connection timeout = 1000s

info_string = """
    select articles.id, articles.content_id, articlecontent.content
    from NewsCollectorInfo.articles 
    join NewsCollectorInfo.articlecontent on articles.content_id = articlecontent.id """
    
if cur != None:

    try:
        cur.execute(info_string)
        print("Article contents retrieved from db")
        all_info = cur.fetchall()
    except (Exception, Error) as error:
        print("\nexecute_sql() error:", error)
        conn.rollback()


# Load LDA Model and Dictionary
lda_file_path = 'lda_models/' + num_topics + '_topics/gensim_lda_model'
lda_model = LdaMulticore.load(lda_file_path)
dict_pickle = open("lda_dictionary/30_topics/dict.pickle","rb")
dictionary = pickle.load(dict_pickle)

progress_iter = 0
# Iterate through articles and extract the appropriate information
for i in range(len(all_info)): # Starts at 0

    # Loading bar in stdout
    progress(progress_iter, len(all_info), 'Assigning topics to articles')

    # Extract the article ID 
    article_id = all_info[i][0]

    # Test article content on LDA model
    article_content = all_info[i][2] 
    bow_vector = dictionary.doc2bow(preprocess(article_content))
    
    # We extract the most strongly correlated topic ID for the article
    # Note: We need to add 1 because the ID's in thenewsroom_database start at 1, 
    # and the ID's in the LDA model start from 0! GROSS, FIX THIS

    lda_output = sorted(lda_model[bow_vector], key=lambda topic: topic[1], reverse = True)
    articles_topic_id = lda_output[0][0] + 1 

#---------------------------------------------------------------------------------
    
# HACKY APPROACH TO COMBINING ID's FOR FOOTBALL AND ASSIGNING TO TOPIC ID = 3
    
    if articles_topic_id in (15, 24): # Football
        articles_topic_id = 10
    elif articles_topic_id in (21, 29): # Us Politics
        articles_topic_id = 2
    elif articles_topic_id in (17, 22):  # Coronavirus
        articles_topic_id = 7
    elif articles_topic_id == 25: # Crime
        articles_topic_id = 5
#---------------------------------------------------------------------------------
    
    IDs = (articles_topic_id, article_id)
    
    topicofarticle_insert_string = """INSERT INTO NewsCollectorInfo.topicofarticle 
                                      (topic_id, article_id) VALUES (%s, %s)"""
    
    cur.execute(topicofarticle_insert_string, IDs)
    conn.commit()
    
    progress_iter += 1
    
# close the cursor and connection
cur.close()
conn.close()      
print('\n')











