# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:36:08 2024

@author: capat
"""

import sqlite3
from datetime import datetime

def fix_date(x):
    return(datetime.strptime(x[1], '%d/%m/%Y').date().strftime('%Y-%m-%d'), x[0])

conexion = sqlite3.connect("cash.db")
cursor = conexion.cursor()

cursor.execute("SELECT cid, date FROM currency" )
datos = cursor.fetchall()
fixed = list(map(fix_date, datos))
cursor.executemany("UPDATE currency SET date = ? WHERE cid = ?", fixed)
conexion.commit()

cursor.execute("SELECT id, date FROM prices" )
datos_p = cursor.fetchall()
fixed_p = list(map(fix_date, datos_p))
cursor.executemany("UPDATE prices SET date = ? WHERE id = ?", fixed_p)
conexion.commit()
conexion.close()
