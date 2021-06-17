#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 20:09:43 2020

@author: Jono

This function obtains the number of articles in thenewsroom_database

"""

from psycopg2 import connect, Error

#------------------ Connect to thenewsroom_database ------------------#

def thenewsroom_db_num_articles():

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
    
#------------- Retrieve number of articles in database ---------------#
    
    # only attempt to execute SQL if cursor is valid
    if cur != None:
    
        try:
            cur.execute(""" SELECT COUNT(*) FROM NewsCollectorInfo.Articles """)
            num_articles = cur.fetchone()
            
        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()
    
    # close the cursor and connection
    cur.close()
    conn.close()
        
    return num_articles[0]