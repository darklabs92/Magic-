# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 20:26:00 2017

@author: vsdak
"""

# check if certain timeslots are not availalbe

import pandas as pd
import os
import numpy as np
import datetime

hostname = 'localhost'
username = 'root'
password = ''
database = 'sakila'

# Simple routine to run a query on a database and print the results:

print "Using pymysql…"
import pymysql
myConnection = pymysql.connect( host=hostname, user=username, passwd=password)
with myConnection.cursor() as cursor:
    # The SQL command to be extract all rental related info in the given 'database'
    sql1 = "SELECT * from sakila.rental ;" 
    
    # store the result of the SQL commands into Pandas DF
    rentalPd = pd.read_sql(sql1,myConnection)
    
    # The SQL command to be extract all inventory related info in the given 'database'
    sql2 = "SELECT * from sakila.inventory ;" 
    
    # store the result of the SQL commands into Pandas DF
    inventoryPd = pd.read_sql(sql2,myConnection)
    
    
    # The SQL command to be extract all film related info in the given 'database'
    sql3 = "SELECT * from sakila.film ;" 
    
    # store the result of the SQL commands into Pandas DF
    filmPd = pd.read_sql(sql3,myConnection)
    
    # reference movie name against filmId
    movieTitle = list(filmPd.title)
    filmId = list(filmPd.film_id)
    
    # inventory lookup table
    inventoryId = list(inventoryPd.inventory_id)
    inv_filmId = list(inventoryPd.film_id)
    inv_storeId = list(inventoryPd.store_id)
    
    # rental information
    rentId = list(rentalPd.rental_id)
    rent_invId = list(rentalPd.inventory_id)
    rent_custId = list(rentalPd.customer_id)
    rent_outDate = list(rentalPd.rental_date)
    rent_inDate = list(rentalPd.return_date)
    
    for k in range(len(rent_inDate)):
        if rent_inDate[k]>datetime.datetime.now():
            print rent_custId[k]
