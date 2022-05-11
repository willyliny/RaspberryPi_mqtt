import paho.mqtt.client as mqtt
import time
import config
import pymongo
import schedule
import random
import json


HOST = config.mqtt["host"]
PORT = config.mqtt["port"]

myclient = pymongo.MongoClient(config.mongoDB["db_host"])
myclient = pymongo.MongoClient(config.mongoDB["db_host"])

TOPIC = "test"
DATABASE_NAME = "PD_TEST"
COLLECTION_NAME = "DEVICE_RECORD"

def updateMongo(data):
    mydb = myclient[DATABASE_NAME]
    mycollection = mydb[COLLECTION_NAME]
    count=0

    if mycollection.find():
        for post in mycollection.find():
            count += 1
            data['_id'] = count
            print('id = ',count)
    
    mycollection.insert_one(data)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC)
    # client.subscribe("test1")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))

    print(msg.topic+" "+msg.payload.decode("utf-8"))
    print('data: \n{}'.format(data))
    updateMongo(data)
    print(client_id)
    
    if (msg.payload.decode("utf-8") == "stop"):
        client.disconnect()
    

client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
client = mqtt.Client(client_id)   #clientID can't repeat
client.username_pw_set(config.mqtt["admin"], config.mqtt["password"])  
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(HOST, PORT, 60)



if __name__ == '__main__':
    client.loop_forever()