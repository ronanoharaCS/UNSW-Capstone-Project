#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:38:15 2020

@author: admin
"""


from psycopg2 import connect, Error

#------------------ Connect to thenewsroom_database ------------------#

def retrieve_article_content():

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
    
    #------------- Retrieve article content for processing ---------------#
    
    # only attempt to execute SQL if cursor is valid
    if cur != None:
    
        try:
            cur.execute(""" SELECT content FROM NewsCollectorInfo.ArticleContent """)
            ArticleContent_All = cur.fetchall()
            print("Article content retrieved")
            
        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()
    
    # close the cursor and connection
    cur.close()
    conn.close()
    
    # Convert ArticleContent_All from list of tuples, to list of strings
    for i in range(len(ArticleContent_All)):
        ArticleContent_All[i] = ArticleContent_All[i][0]    
    
    
    return ArticleContent_All # Contains list of articles contents to be processed