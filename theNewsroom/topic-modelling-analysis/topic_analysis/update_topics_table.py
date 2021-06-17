#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:30:21 2020

@author: Jono

This function inserts the topics and their respective ID's into 
thenewsroom_database.topics table

"""


from psycopg2 import connect, Error
from functions.connect_to_db import connect_to_thenewsroom_db

#------------------ Connect to thenewsroom_database ------------------#

print ('Connecting to thenewsroom_database')
conn, cur = connect_to_thenewsroom_db(10) # connection timeout = 10s

#------------- Retrieve article content for processing ---------------#

# Topics Table
topics_format_string = """INSERT INTO NewsCollectorInfo.Topics 
                                    (id, name) 
                                VALUES 
                                    (%s, %s);"""

# thenewsroom_topics = (
    
#     (1, 'Economics'),
#     (2, 'Golf'),
#     (3, 'Football'),
#     (4, 'Middle East'),
#     (5, 'Sydney'),
#     (6, 'Technology'),
#     (7, 'Horse Racing'),
#     (8, 'Rugby'),
#     (9, 'Middle East'),
#     (10, 'Business'),
#     (11, 'Hunting'),
#     #(12, 'Football'),
#     (13, 'Dancing'),
#     (14, 'Surfing'),
#     #(15, 'Football'),
#     (16, 'British Politics'),
#     (17, 'The Great British Bake Off'),
#     #(18, 'Football'),
#     (19, 'Art'),
#     (20, 'Sexual Harassment'),
#     (21, 'Adani'),
#     (22, 'Asylum Seekers and Refugees'),
#     (23, 'Stephen Bannon'),
#     (24, 'Journalism'),
#     #(25, 'Football'),
#     (26, 'Australian Politics'),
#     (27, 'Cricket'),
#     #(28, 'Football'),
#     #(29, 'Football'),
#     (30, 'Terrorism'),
#     (31, 'Uber'),
#     (32, 'Film'),
    
# )

# Manually create a list 
thenewsroom_topics = (
    
    (1, 'Economy'),
    (2, 'US Politics'),
    (3, 'China'),
    (4, 'Law'),
    (5, 'Crime'),
    (6, 'Bushfires'),
    (7, 'Coronavirus'),
    (8, 'Golf'),
    (9, 'Climate Change'),
    (10, 'Football'),
    (11, 'Travel'),
    (12, 'Retail'),
    (13, 'Film and Music'),
    (14, 'Black Lives Matter'),
    #(15, 'Football'),
    (16, 'Education'),
    #(17, 'Coronavirus'),
    (18, 'Rugby'),
    (19, 'Technology'),
    (20, 'Housing'),
    #(21, 'US Politics'),
    #(22, 'Coronavirus'),
    (23, 'Cricket'),
    #(24, 'Football'),
    #(25, 'Crime'),
    (26, 'Tennis'),
    (27, 'British Politics'),
    (28, 'Horse Racing'),
    #(29, 'US Politics'),
    (30, 'Charity'),
    
)


# only attempt to execute SQL if cursor is valid
if cur != None:

    try:

        # for topic in test_topics:
        #     cur.execute(topics_format_string, (topic,))                       
        #     conn.commit()
        cur.executemany(topics_format_string, thenewsroom_topics)
        print("INSERT SUCCESS")
        conn.commit()
    except (Exception, Error) as error:
        print("\nexecute_sql() error:", error)
        conn.rollback()

# close the cursor and connection
cur.close()
conn.close()



