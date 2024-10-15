# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:44:08 2024

@author: capat
"""

import sqlite3
from itertools import chain
import pandas as pd

def get_names(opcion):
    conexion = sqlite3.connect("cash.db")
    cursor = conexion.cursor()
    if opcion == 'moneda':
        cursor.execute("SELECT DISTINCT curname FROM currency")
    elif opcion == 'acciones':
        cursor.execute("SELECT DISTINCT name FROM prices")
    nombres = list(chain(*cursor.fetchall()))
    conexion.close()
    return(nombres)

def get_data(name, daterange):
    conexion = sqlite3.connect("cash.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT AVG(price),MIN(price), MAX(price) FROM currency WHERE curname = ? AND date BETWEEN ? AND ?", (name,daterange[0],daterange[1]))
    try:
        datos = tuple(map(lambda x: round(x,2), chain(*cursor.fetchall())))
    except TypeError:
        datos = None
        
    conexion.close()
    return(datos)

def get_money(daterange):
    conexion = sqlite3.connect("cash.db")
    return(pd.read_sql_query("SELECT date, curname, price FROM currency WHERE date BETWEEN ? AND ?", conexion, params = (daterange[0],daterange[1]), parse_dates = {'date' : {'format' : '%Y-%m-%d'}}))

def get_table(name):
    conexion = sqlite3.connect("cash.db")
    return(pd.read_sql_query("SELECT date, name, price FROM prices WHERE name = ?", conexion, params = [name], parse_dates = {'date' : {'format' : '%Y-%m-%d'}}))
    
def get_latest():
    conexion = sqlite3.connect('cash.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(date) FROM prices")
    maxdate = cursor.fetchone()[0]
    conexion.close()
    return maxdate