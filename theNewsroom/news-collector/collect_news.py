#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:37:11 2020

@author: z5079346

This script retrieve's data from select news API's
and inserts the data into thenewsroom_database (postgreSQL)

"""

import requests
import json, sys
from psycopg2 import connect, Error
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta
import enum
import collections
from datetime import datetime


#--------------------------- API HashMap's ---------------------------#

class Guardian():

    def __init__(self):
        
        self.name = "Guardian"
        self.id = 1
        self.page_limit = 200
        self.url = 'https://content.guardianapis.com/search?'
        self.api_key_liam = '08efafef-c5c0-43c6-a00e-b67880b448b2'
        self.api_key_jono = '450f355e-ac29-4a67-88d0-b72275c1c8c8'

        # Hashmap maps (ourSQLSchemaColumnName, GuardianAPIField)
        self.HashMap = collections.OrderedDict([ 
                            ('article_type'      , 'type' ),   
                            ('publication_date'  , 'webPublicationDate'),
                            #('api_given_topic'   , 'sectionName'),
                            ('title'             , 'webTitle'),
                            ('web_content_url'   , 'webUrl'),
                            ('media_outlet_id'   , self.id      ),
                            ('content_id'        , 0      ) # 0 is a placeholder
                            ])     
            
#------------------------- Retrieve API Data -------------------------#

# Create instances of each API class
Guardian_test = Guardian()

# List containing all the instances of API's
APIs = [Guardian_test]

# For each API, retrieve data
for API in APIs:

    print("Collecting " + str(API.page_limit) + " pages from the " + API.name +" API")
    
    params = {
        #'q'                 : 'trump',
        'from-date'         :    "2020-10-13",
        'to-date'           :    "2020-10-13",
        'api-key'           :API.api_key_liam,
        'page-size'         :  API.page_limit,     # 200 = max page size for Guardian
        'show-editors-picks':          'true',
        'show-elements'     :         'image',
        'show-fields'       :           'all',
    }

    # Retrieve data from the media outlet
    response = requests.get(API.url, params=params)
    data = response.json()
    all_results = []
    all_results.extend(data['response']['results'])
    
    # Extract the article content (text) and given Topic
    article_content = []
    article_topics = []
    for article in all_results:
        article_content.append(article['fields']['bodyText'])
        article_topics.append(article['sectionName'])
    
    # Convert webPublicationDate from unicode to datetime type
    if API.name == 'Guardian':
        for article in all_results:
            article['webPublicationDate'] = datetime.strptime(article['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ').date()


    # Remove unwanted attributes from all_results 
    for article in all_results:
        for info in list(article):
            if info not in API.HashMap.values():
                del article[info]

    # Enumerate the article_type attribute (required for thenewsroom_database)
    article_enum = {'type': 'Opinion'}  # PLACEHOLDER. NEEDS FIXING
    
    for article in all_results:
        article.update(article_enum)
    
#--------------  Convert API results into an SQL query ---------------#
    
    # create a nested list of the articles
    articles = [list(x.values()) for x in all_results] 
    
    # Append the API id to each article 
    for article in articles:
        article.append(API.id)    
           

    # Create queries to be INSERT'ed into the postgres database

    
    # https://stackoverflow.com/questions/5247685/python-postgres-psycopg2-getting-id-of-row-just-inserted
    # Articles Table
    column_names = ", ".join(API.HashMap.keys())
    value_format_string = ("%s," * len(API.HashMap))[:-1]
    articles_row_format_string = """INSERT INTO NewsCollectorInfo.Articles 
                                        ({}) 
                                    VALUES 
                                        ({}) 
                                    RETURNING id;""".format(column_names, value_format_string)
    
    # ArticleContent Table
    content_row_format_string = """INSERT INTO NewsCollectorInfo.ArticleContent 
                                        (content) 
                                    VALUES 
                                        (%s)
                                    RETURNING id;"""
    
    # Topics Table
    topic_row_format_string = """INSERT INTO NewsCollectorInfo.Topics 
                                        (name) 
                                    VALUES 
                                        (%s)
                                    RETURNING id;"""

#------------------ Connect to thenewsroom_database ------------------#

    
    print ('Connecting to thenewsroom_database')
    try:
        # declare a new PostgreSQL connection object
        conn = connect(
            dbname = "thenewsroom_database",
            user = "postgres",
            host = "127.0.0.1",
            password = "password",
            # attempt to connect for 3 seconds then raise exception
            connect_timeout = 3
        )
        cur = conn.cursor()
            
    except (Exception, Error) as err:
        print ("Failed to connect to thenewsroom_database \npsycopg2 connect error:", err)
        conn = None
        cur = None
    
    
#------------------------- Execute SQL INSERT ------------------------#
    

    # only attempt to execute SQL if cursor is valid
    if cur != None:
    
        try:
           
            # Insert each article into the appropiate tables
            for article, content, topic in zip(articles, article_content, article_topics):
                
                # insert article contents
                cur.execute(content_row_format_string, (content,)) # Formatting: Needs to be a tuple (or list)
                # added RETURNING to statements
                content_id = cur.fetchone()[0]
                         
                article.append(content_id)
                
                # insert article
                cur.execute(articles_row_format_string, article)
                article_id = cur.fetchone()[0]
                
                # insert article topic 
                # need to check if it already exists
                cur.execute(""" SELECT * 
                                    FROM NewsCollectorInfo.Topics 
                                    WHERE (name LIKE %s);               
                            """, (topic,))

                topic_id = cur.fetchone()
                if not topic_id:
                    cur.execute(topic_row_format_string, (topic,))
                    topic_id = cur.fetchone()[0]
                else:
                    topic_id = topic_id[0]
                    
                # insert ids as foreign keys into topicofarticle table
                topicofarticle_format_string = """INSERT INTO NewsCollectorInfo.TopicOfArticle (topic_id, article_id) VALUES (%s, %s)"""
                cur.execute(topicofarticle_format_string, (topic_id, article_id))
                
            conn.commit()
    
            print ('INSERT SUCCESS' )
    
        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()
        
        # close the cursor and connection
        cur.close()
        conn.close()
    

