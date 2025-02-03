# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:46:07 2024

@author: capat
"""

from shiny import App, render, ui, reactive, req
from sqlitefun import get_names, get_data, get_table, get_money, get_latest
#from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpldates

nombres = get_names('moneda')
acciones = get_names('acciones')

app_ui = ui.page_fluid(
    ui.panel_title("Indicadores financieros", "Indicadores"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("moneda", "Moneda", nombres),
            ui.input_date_range("fechas", "Fechas", format = 'dd-mm-yyyy', max = get_latest()),
            ui.input_action_button("calcular", "Calcular")
            ),
        ui.output_text("salida"),
        ui.output_plot("plotmon")
        ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select('acciones', 'Acciones', acciones)
            ),
        ui.output_plot('lineplot', height="400px")
        ),
    ui.output_table('resacciones')
    )

def server(input, output, session):
    
    @render.text
    @reactive.event(input.calcular)
    def salida():
        datos = get_data(input.moneda(), input.fechas())
        if datos is None:
            return "No hay información para las fechas seleccionadas"
        else:
            return f"El valor promedio del {input.moneda()} es:\n${datos[0]}, con un mínimo de ${datos[1]} y un máximo de ${datos[2]}"
    
    @render.table
    def resacciones():
        req(input.acciones())
        tabla = get_table(input.acciones())
        return(tabla)
    
    @render.plot
    def lineplot():
        req(input.acciones())
        df = get_table(input.acciones())
        fig, ax = plt.subplots()
        ax.plot('date','price', data = df)
        ax.set_ylabel('Precio (COP)')
        ax.set_xlabel('Fecha')
        ax.xaxis.set_major_locator(mpldates.MonthLocator())
        return(fig)
    
    @render.plot
    @reactive.event(input.calcular)
    def plotmon():
        datos = get_money(input.fechas())
        datos = pd.pivot(datos, index = 'date', columns = 'curname', values = 'price')
        fig, ax = plt.subplots(ncols=1, nrows=len(datos.columns))
        for i in range(len(datos.columns)):
            ax[i].plot(datos.index, datos[datos.columns[i]])
            ax[i].set_title(datos.columns[i])
            ax[i].set_ylabel('Precio (COP)')
            ax[i].set_xlabel('Fecha')
            ax[i].xaxis.set_major_locator(mpldates.MonthLocator())
            
        return(fig)
    
app = App(app_ui, server)

app.run()