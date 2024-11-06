# Importación de módulos necesarios para el funcionamiento de Dash y la visualización de gráficos.
from dash import Output, Input, State, no_update, callback
import pandas as pd
import plotly.express as px
import json
from plotly import graph_objects as go
from dash import dcc
from dash import Patch
#from gdash2 import app
from glob import glob

# Importación de la base de datos MongoDB usando pymongo
import pymongo

# Cadena de conexión a MongoDB Atlas
conn = "mongodb+srv://ger:iaci2023@cluster0.jghr8.mongodb.net/"

# Creación de la instancia de cliente de MongoDB para conectarse a la base de datos
mongo_client = pymongo.MongoClient(conn)

# Selección de la base de datos y la colección dentro de MongoDB
db = mongo_client.sensor # Selecciona la base de datos 'sensor'
tabla = db.sensor         # Selecciona la colección 'sensor' dentro de la base de datos
tabla.find()              # Realiza una búsqueda inicial (opcional)

# Función para abrir un archivo JSON y convertirlo en un DataFrame de pandas
def openJsonAsDf(Jdata):
    # Carga los datos desde el archivo JSON
    with open(str(Jdata),'r') as json_file:
        Jdata3 = json.load(json_file)
    
    # Elimina el campo 'deviceId' del diccionario cargado
    Jdata3.pop('deviceId')
    
    # Imprime la longitud de cada campo en el diccionario
    for k, v in Jdata3.items():
        print(f"{k}: {len(v)}")
    
    # Devuelve el diccionario como un DataFrame de pandas
    return pd.DataFrame(Jdata3)

# Importación de funciones específicas desde el módulo 'BaseDatos'
from BaseDatos import (
    get_dic_from_selected_val,
    get_data_files_names
)

#-------------------- Levantar nombres de dispositivos -----------------------
@callback(
    Output('dropSensor', 'options'),  # Salida para actualizar las opciones del dropdown de sensores
    Input('intervalo-actualizacion', 'n_intervals'),  # Entrada: intervalo de actualización
)
def uptade_names(n_intervals):
    """Levanta nombres de los sensores desde la base de datos."""
    # Llama a la función que obtiene los nombres de sensores
    names = get_data_files_names()
    
    # Formatea los nombres como opciones para el dropdown
    opciones = [{'label': n, 'value': n} for n in names]
    
    return opciones

#-------------------- Elegir Sensor -----------------------
@callback(
    Output('data-store', 'data'),  # Salida: almacenamiento de datos en dcc.Store
    Input('dropSensor', 'value'),  # Entrada: valor seleccionado en el dropdown de sensores
    Input('intervalo-actualizacion', 'n_intervals'),  # Entrada: intervalo de actualización
)
def update_output(valor, n_interval):
    """Actualiza el almacenamiento de datos en función del sensor seleccionado."""
    # Si no hay un sensor seleccionado, no realiza ninguna actualización
    if valor is None:
        return no_update
    
    # Llama a la función que obtiene datos específicos del sensor seleccionado desde MongoDB
    dic = get_dic_from_selected_val(valor)
    
    return dic

#-------------------- Elegir Variable -----------------------
@callback(
    Output('dropVar', 'options'),  # Salida: opciones para el dropdown de variables
    Input('data-store', 'data')  # Entrada: datos almacenados en dcc.Store
)
def actualizar_opciones(datos):
    """Actualiza las opciones en el dropdown de variables basándose en los datos disponibles."""
    # Verifica si hay datos almacenados
    if datos:
        l0 = []  # Lista para almacenar los nombres de columnas únicas
        for k, v in datos.items():
            l0 = l0 + list(v.keys())
        
        # Convierte la lista a un conjunto para eliminar duplicados
        l0 = set(l0)
        
        # Elimina las columnas 'tiempo' o 'Tiempo' si están presentes
        if 'tiempo' in l0:
            l0.remove('tiempo')
        if 'Tiempo' in l0:
            l0.remove('Tiempo')
        
        print(l0)  # Imprime la lista de variables para depuración
        opciones = [{'label': col, 'value': col} for col in l0]  # Formatea opciones para dropdown
    else:
        opciones = []
    
    return opciones

#------------------ Generación de Gráficos -----------------
@callback(
    Output('figures-container', 'children'),  # Salida: contenedor de gráficos
    Input('dropVar', 'value'),  # Entrada: variables seleccionadas en dropdown de variables
    Input('data-store', 'data'),  # Entrada: datos almacenados en dcc.Store
    prevent_initial_call=True  # Previene el llamado inicial hasta que haya datos
)
def create_graph(selected_column, datos):
    """Crea gráficos en función de las variables seleccionadas."""
    figs = []  # Lista para almacenar los gráficos generados
    
    # Si no hay datos almacenados, devuelve None
    if datos == {}:
        return None
    
    # Si no hay columna seleccionada, no realiza ninguna actualización
    if selected_column is None:
        return no_update
    
    # Itera sobre cada variable seleccionada para crear gráficos individuales
    for sel in selected_column:
        fig = go.Figure()  # Crea una nueva figura en Plotly
        
        # Itera sobre cada sensor en los datos
        for datos_key, datos_val in datos.items():
            df = pd.DataFrame(datos_val)  # Convierte los datos del sensor en un DataFrame
            
            # Verifica si la columna seleccionada existe en el DataFrame
            if sel in df.columns:
                xx = 'Tiempo'  # Eje X representa el tiempo
                yy = sel       # Eje Y representa la variable seleccionada
                
                # Crea una línea de tiempo con los datos de la variable seleccionada
                this_line = go.Scatter(
                    x = df[xx],
                    y = df[yy],
                    name = f'{datos_key}'  # Nombre de la línea basado en el sensor
                )
                
                # Si hay datos, agrega la línea al gráfico y configura el layout
                if yy is not None:
                    fig.add_trace(this_line)
                    fig.update_layout(
                        title = f'{yy}',
                        title_font = dict(size=24, color='white'),  # Estilo del título
                        title_x = 0.5,  # Centrado
                        template = 'plotly_dark'  # Tema oscuro para el gráfico
                    )
        
        # Agrega el gráfico al contenedor de gráficos
        g = dcc.Graph(
            figure = fig,
            id = {'type': 'graph', 'id': sel}  # Asigna un id único al gráfico
        )
        
        figs.append(g)  # Añade el gráfico a la lista de gráficos
    
    return figs
