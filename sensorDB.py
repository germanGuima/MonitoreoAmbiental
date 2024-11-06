#########################################################################
#----------------------- Conexión a la Base de Datos --------------------------------------------#
import pymongo
from pymongo import MongoClient
from datetime import datetime
import pprint

# Establecer conexión con MongoDB Atlas utilizando la URI de conexión
conn = "mongodb+srv://ger:iaci2023@cluster0.jghr8.mongodb.net/"
mongo_client = pymongo.MongoClient(conn)

# Crear o acceder a la base de datos y la colección
db = mongo_client.sensor  # Selecciona la base de datos llamada 'sensor'
tabla = db.sensor         # Selecciona la colección llamada 'sensor' dentro de la base de datos

# Recuperar los nombres únicos de dispositivos para usarlos en la aplicación
todos_nombres = [val['deviceId'] for val in tabla.find({}, {'deviceId': 1, '_id': 0})]
nombres_unicos = list(set(todos_nombres))  # Eliminar duplicados para obtener nombres únicos

# Comprobar si hay dispositivos en la colección y recuperar todos los datos del primero si existen
if nombres_unicos:
    todosLosDatosDelPrimerNombreUnico = list(tabla.find({'deviceId': nombres_unicos[0]}))
else:
    print("La lista 'nombres_unicos' está vacía. No se puede acceder al primer elemento.")

#########################################################################
#----------------------- Conexión MQTT --------------------------------------------#
import json
import paho.mqtt.client as mqtt

# Función para insertar datos en la base de datos
def insertarBase(data):
    """Inserta un documento en la base de datos MongoDB."""
    try:
        val = tabla.insert_one(data)
        return val
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
        return None

# Función de callback que se ejecuta al recibir un mensaje MQTT
def on_message(mqtt_client, userdata, message):
    """Procesa los mensajes entrantes desde el broker MQTT."""
    # Decodificar el mensaje recibido
    msg = str(message.payload.decode("utf-8"))
    print("Mensaje recibido =", msg)
    try:
        # Convertir el mensaje JSON en un diccionario de Python
        Jmsg = json.loads(msg)
        
        # Agregar un campo de tiempo con la fecha y hora actual
        Jmsg['Tiempo'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar el mensaje en la base de datos
        val = insertarBase(Jmsg)
        if val:
            print('Valor guardado en la base de datos:', val.inserted_id)
        else:
            print("No se pudo guardar el mensaje en la base de datos.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Configuración del cliente MQTT
broker_address = "4a98668d55074575a6e66b180cc7b6b2.s1.eu.hivemq.cloud"  # Dirección del broker
port = 8883  # Puerto de conexión para MQTT seguro (TLS)
usuario = {'username': 'german', 'password': 'German1234'}  # Credenciales de usuario

# Crear cliente MQTT y configurar credenciales
mqtt_client = mqtt.Client(userdata=usuario)
mqtt_client.username_pw_set(usuario['username'], usuario['password'])

# Configurar TLS para una conexión segura
mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# Conectar al broker MQTT
mqtt_client.connect(broker_address, port)

# Asignar la función de callback para manejar los mensajes recibidos
mqtt_client.on_message = on_message

# Suscribirse al tópico para recibir mensajes
mqtt_client.subscribe("a")

# Publicar un mensaje inicial para indicar la conexión
pub = mqtt_client.publish("a", "PC:Estoy Viendo")
if pub.is_published():
    print("Mensaje publicado correctamente")
else:
    print("No se pudo publicar el mensaje")

# Iniciar el bucle para escuchar mensajes de forma continua
mqtt_client.loop_forever()
