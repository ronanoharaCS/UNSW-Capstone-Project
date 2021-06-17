#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 20:20:23 2020

@author: Jono

Function to connect to thenewsroom_database

"""

from psycopg2 import connect, Error


def connect_to_thenewsroom_db(connection_limit_seconds):
    
    print ('Connecting to thenewsroom_database')
    try:
        # declare a new PostgreSQL connection object
        conn = connect(
            dbname = "thenewsroom_database",
            user = "postgres",
            host = "127.0.0.1",
            password = "password",
            # attempt to connect for 'x' seconds then raise exception
            connect_timeout = connection_limit_seconds
        )
        cur = conn.cursor()
            
    except (Exception, Error) as err:
        print ("Failed to connect to thenewsroom_database \npsycopg2 connect error:", err)
        conn = None
        cur = None
        
    return conn, cur

