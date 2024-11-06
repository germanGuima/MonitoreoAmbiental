#########################################################################
#-----------------------Base-de-datos--------------------------------------------#
import pymongo
import pprint
import datetime as dt
# Establish connection
import time
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://ger:iaci2023@cluster0.vxyuxqk.mongodb.net/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['user_shopping_list']

# Create a database
db = client.classDB
 # sensor --> NodeMCU
# db.sensor.insert_one(
#     {
#         'deviceId':'NodeMCU',
#         'Humedad':'0',
#         'Temperatura':'0',
#         'Co2_ppm':'0',
#         'time':time.time(),
#       }
# )
# listaSensor = list(db.sensor.find({'deviceId':'NodeMCU'}))
# sensor1=listaSensor[0]

from pymongo import MongoClient
import json

#########################################################################
#----------------------Mqtt------------------------------------------------------------------

import paho.mqtt.client as mqtt 
#import the client1 
broker_address="4a98668d55074575a6e66b180cc7b6b2.s1.eu.hivemq.cloud" #use external broker
port=8883
usuario= {'username':'german',
             'password':'German1234'}

client = mqtt.Client(userdata=usuario)#mqtt.Client("P1") #create new instance
#usar identificador para multiples clientes 
client.username_pw_set("german","German1234")
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.connect(broker_address,port) #connect to broker
pub=client.publish("a","PC:Estoy Viendo")
print(pub.is_published())

def on_message(client, userdata, message):
    #funcion que se ejecuta cuando recibe un mensaje
    msg = str(message.payload.decode("utf-8"))
    print("received message =",msg)
    #msg_json ... #json.loads(msg)
    Jmsg=json.loads(msg)
    #print(Jmsg["temperatura"])
    #print(Jmsg["humedad"])

    Ntemp=Jmsg['temperatura']
    Nhum=Jmsg['humedad']
    Nco2=Jmsg['Co2_ppm']

    print(Ntemp)
    print(Nhum)
    print(Nco2)
#pasar de on_message a nuevos valores  # Json 
    # nuevos_valores = { 
    #                 "$set": { 'Humedad': Nhum},
    #                 "$set": { 'Temperatura': Ntemp},
    #                 "$set": { 'Co2_ppm': Nco2},
    #                 "$set": { 'time':time.time()},
    #                 }
    nuevos_valores = { 
                    'deviceId': 'NodeMCU',# esto debería ser la id de cada sensor
                    'Humedad': Nhum,
                    'Temperatura': Ntemp,
                    'Co2_ppm': Nco2,
                    'time':time.time(),
                    }



# Realizar la actualización
    #filter = { 'deviceId': 'NodeMCU' }
    #result = db.sensor.update_one(filter, nuevos_valores)
    db.sensor.insert_one(nuevos_valores)
    print('valor guardado')


dicc={'Hum':[],
'co2':[],
'tiempo' : [],
'temp':[],
}
for i,post in enumerate(db.sensor.find()):
    print(post.keys())
    dicc['co2'].append(post['Co2_ppm'])
    dicc['tiempo'].append(post['time'])
    dicc["Hum"].append(post['Humedad'])
    dicc['temp'].append(post['Temperatura'])




# Verificar si se realizó la actualización correctamente
    # if result.modified_count > 0:
    ruta_del_archivo = "/home/ger/Escritorio/dashV2/data/datos.json"
    #     # Guardar el JSON en el archivo
    with open(ruta_del_archivo, "w") as archivo:
             json.dump( dicc, archivo)
    #     print('Documento actualizado correctamente.')
    # else:
    #   print('No se encontró ningún documento que coincida con el filtro.')

   


client.on_message = on_message #Mensaje Recibido -Guardar en base de datos
client.subscribe("a")

client.loop_forever() 

