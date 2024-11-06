#########################################################################
#-----------------------Base-de-datos--------------------------------------------#
import pymongo
import pprint
import datetime as dt
from pymongo import MongoClient
# Establish connection
import time
conn = "mongodb://localhost:27017"
mongo_client = pymongo.MongoClient(conn)

# def get_database():
 
#    # Provide the mongodb atlas url to connect python to mongodb using pymongo
#    CONNECTION_STRING = "mongodb+srv://ger:iaci2023@cluster0.vxyuxqk.mongodb.net/"
 
#    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
#    client = MongoClient(CONNECTION_STRING)
 
#    # Create the database for our example (we will use the same database throughout the tutorial
#    return client['Dispositivos']

# Create a database
db = mongo_client.sensorsDB#classDB


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

mqtt_client = mqtt.Client(userdata=usuario)#mqtt.Client("P1") #create new instance
#usar identificador para multiples clientes 
mqtt_client.username_pw_set("german","German1234")
mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
mqtt_client.connect(broker_address,port) #connect to broker
pub=mqtt_client.publish("a","PC:Estoy Viendo")
print(pub.is_published())


#####################funcion que se ejecuta cuando recibe un mensaje####################################################
diccSensores={}
dicc={}
def on_message(mqtt_client, userdata, message):
    #funcion que se ejecuta cuando recibe un mensaje
    msg = str(message.payload.decode("utf-8"))
    print("received message =",msg)
    #msg_json ... #json.loads(msg)
    Jmsg=json.loads(msg)

    
    # #pares nombres el que viene de mqtt y a donde va a parar a db
    # pares_nombres= {'temperatura': 'Temperatura',
    #                 'humedad':'Humedad',
    #                 'Co2_ppm':'Co2_ppm',
    #                 'lux':'lux',
    #                 'deviceId':'deviceId'}
    
    # Ntemp=Jmsg['temperatura']
    # Nhum=Jmsg['humedad']
    # Nco2=Jmsg['Co2_ppm']
    # #Nlux=Jmsg['lux']
    # NId=Jmsg['deviceId']
   
    Jmsg['tiempo'] = time.time()
    # nuevos_valores ={'tiempo': time.time()}
    

    # nuevos_valores = { 
    #                 'deviceId': NId,
    #                 'Humedad': Nhum,
    #                 'Temperatura': Ntemp,
    #                 'Co2_ppm': Nco2,
    #                 'tiempo':time.time(),
    #                 }
    db.sensor.insert_one(Jmsg)
  
    print('valor guardado---------------')

#aca se completan los diccionarios
    for i,post in enumerate(db.sensor.find()):
        # print(post.keys())
        curr_id = post['deviceId']
        curr_dic = diccSensores.get(curr_id,{})

        for key, val in post.items(): 
            print(key)
            # print(val)
            if not key in dicc:
                dicc[key] = [val] 
            else:
                if key not in ['_id','deviceId']:
                    dicc[key].append(val)

    #objectID es lista ,no json serializable
 
    del dicc['_id']
    #print(dicc['time'])

    diccSensores[curr_id] = curr_dic
    # print('  diccSensores:')
    # print(diccSensores)    
# Verificar si se realizó la actualización correctamente
    # if result.modified_count > 0:
    
    directorio = "/home/ger/Escritorio/dashV2/data/"
    nombre_archivo= str(curr_id) +'.json'
    ruta_del_archivo= directorio+nombre_archivo

        # Guardar el JSON en el archivo

    with open(ruta_del_archivo, "w") as archivo:
        json.dump( dicc, archivo)
        print('Documento actualizado correctamente.')

        # else:
            # print('No se encontró ningún documento que coincida con el filtro.')


mqtt_client.on_message = on_message #Mensaje Recibido -Guardar en base de datos
mqtt_client.subscribe("a")

mqtt_client.loop_forever() 

