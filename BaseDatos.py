# Archivo para gestionar operaciones de lectura y escritura en la base de datos MongoDB
#########################################################################
#----------------------- Base de datos --------------------------------------------#
import pymongo
import pprint
import datetime as dt
from pymongo import MongoClient
import time
import pandas as pd
import json

# Establece la conexión con MongoDB
# conn variable para conexión a base de datos remota en MongoDB Atlas
conn = "mongodb+srv://ger:iaci2023@cluster0.jghr8.mongodb.net/"
mongo_client = pymongo.MongoClient(conn)

# Crear o acceder a la base de datos y colección
db = mongo_client.sensor  # Selecciona o crea la base de datos 'sensor'
tabla = db.sensor         # Selecciona o crea la colección 'sensor'

# Consulta inicial (sin operaciones) para verificar la colección
tabla.find()

# Función para insertar documentos en la colección 'sensor'
def insertarBase(mens):
    """Inserta un documento en la base de datos si no existe, para evitar duplicados."""
    if db.sensor.find():  # Verifica si existen documentos en la colección
        return db.sensor.insert_one(mens)  # Inserta un documento en la colección
    else:
        return False  # Retorna False si ya existe en la base de datos

# Función para convertir una lista de elementos a un diccionario de listas
def parse_dic_from_elems(lista_elems):
    """Convierte una lista de documentos MongoDB en un diccionario de listas, 
    eliminando columnas innecesarias y vacías."""
    df = pd.DataFrame(lista_elems)  # Convierte la lista en un DataFrame de pandas
    
    # Eliminar columnas '_id' y 'deviceId' si están presentes
    if '_id' in df:
        df.drop('_id', axis=1, inplace=True)
    if 'deviceId' in df:
        df.drop('deviceId', axis=1, inplace=True)
        
    # Eliminar columnas vacías
    df.dropna(axis=1, how='all', inplace=True)
    
    return df.to_dict(orient='list')  # Convierte el DataFrame a un diccionario

# Función para recuperar nombres únicos de dispositivos
def get_data_files_names():
    """Consulta todos los 'deviceId' en la colección y retorna una lista con nombres únicos."""
    todos_nombres = [val['deviceId'] for val in tabla.find({}, {'deviceId': 1, '_id': 0})]
    nombres_unicos = list(set(todos_nombres))  # Elimina duplicados para obtener nombres únicos
    return nombres_unicos

# Función para obtener un diccionario de datos de un dispositivo seleccionado
def get_dic_from_selected_val(valor):
    """Recibe una lista de 'deviceId' y devuelve un diccionario de datos para cada uno."""
    dic = {}
    for elemento in valor:
        # Consulta todos los datos del dispositivo actual y los agrega al diccionario
        lista_elems = list(tabla.find({'deviceId': elemento}))
        dic[elemento] = parse_dic_from_elems(lista_elems)  # Convierte los datos en un diccionario
    return dic
