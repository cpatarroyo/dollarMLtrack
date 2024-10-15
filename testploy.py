# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:16:02 2024

@author: capat
"""

import sqlite3
from sqlitefun import get_names, get_data, get_table
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mpldates
from timeit import timeit

tabla = get_table("CARBÓN")

conexion = sqlite3.connect("cash.db")
cursor = conexion.cursor()
cursor.execute("UPDATE currency SET price = price/100 WHERE price > 300000")
conexion.commit()
conexion.close()

conexion = sqlite3.connect("cash.db")
tablam = pd.read_sql_query("SELECT date, curname, price FROM currency", conexion, parse_dates={'date' : {'format' : '%Y-%m-%d'}})
conexion.close()

tablam2 = pd.pivot(tablam, index='date', columns='curname', values='price')

all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

fig, ax = plt.subplots()
ax.plot(tablam2.index,tablam2['EURO'])
ax.plot(tablam2.index,tablam2['TRM'])
#ax.plot(tablam2.index,tablam2['BITCOIN'])
ax.set_ylabel('Precio (COP)')
ax.set_xlabel('Fecha')
ax.xaxis.set_major_locator(mpldates.MonthLocator())
plt.xticks(rotation=30)
plt.show()

datos = tablam
datos = pd.pivot(datos, index = 'date', columns = 'curname', values = 'price')
fig, ax = plt.subplots(ncols=1, nrows=len(datos.columns))
for i in range(len(datos.columns)):
    ax[i].plot(datos.index, datos[datos.columns[i]])
    #ax[i].set_title(datos[datos.columns[i]])
    ax[i].set_ylabel('Precio (COP)')
    ax[i].set_xlabel('Fecha')
    ax[i].xaxis.set_major_locator(mpldates.MonthLocator())
    plt.xticks(rotation=30)



fig, ax = plt.subplots()
ax.boxplot(all_data)

s = """\
import sqlite3
conexion = sqlite3.connect('cash.db')
cursor = conexion.cursor()
cursor.execute("SELECT MAX(date) FROM prices")
maxdate = cursor.fetchone()[0]
conexion.close()
"""

s2 = """\
from sqlitefun import get_latest
maxdate = get_latest()
"""