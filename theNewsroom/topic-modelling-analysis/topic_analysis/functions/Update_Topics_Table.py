#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:30:21 2020

@author: admin

This function inserts the topics and their respective ID's into 
thenewsroom_database.topics table

"""



from psycopg2 import connect, Error

#------------------ Connect to thenewsroom_database ------------------#

def update_topics_table():

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
    
    # Topics Table
    topics_format_string = """INSERT INTO NewsCollectorInfo.Topics 
                                        (id, name) 
                                    VALUES 
                                        (%s, %s);"""
    
    test_topics = (
        (1, 'Coronavirus'),
        (2, 'Trump'),
        (3, 'Willy_Wonka')
    )
    
    # only attempt to execute SQL if cursor is valid
    if cur != None:
    
        try:
            # insert article topic 
            # need to check if it already exists
            # cur.execute(""" SELECT * 
            #                     FROM NewsCollectorInfo.Topics 
            #                     WHERE (name LIKE %s);               
            #             """, (topic,))

            # topic_id = cur.fetchone()
            # if not topic_id:
            #     cur.execute(topic_row_format_string, (topic,)) # topic, is the topic string itself
            #     topic_id = cur.fetchone()[0]
            # else:
            #     topic_id = topic_id[0]
                 
            cur.executemany(topics_format_string, test_topics)

                       
            conn.commit()
            
        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()
    
    # close the cursor and connection
    cur.close()
    conn.close()
    


