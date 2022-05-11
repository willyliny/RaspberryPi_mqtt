from msilib.schema import Feature
from socket import timeout

from click import command
import serial
import time
import json
import random
import schedule
from time import sleep

#defind parameter about Serial (sim7000c)
COM_PORT = "/dev/ttyS0"
BAUD_RATES = 115200
TIMEOUT = 1000
CLIENTID = "20220511"
BROKER_IP = "XXX.XXX.X.XXX:1883"
USERNAME = "admin"
PASSWORD = 123456
TOPIC = "PD"
serial = serial.Serial(COM_PORT, BAUD_RATES, timeout = TIMEOUT)

command_initial = {
    0:'AT',
    1:'AT+CSQ',
    2:'AT+CGNAPN',
    3:'AT+CSTT="internet.iot"',
    4:'AT+CIICR',
    5:'AT+CNACT=1,"internet.iot"',
    6:'AT+CNACT?',
}

command_brokerSetting = {
    0:'AT+SMCONF="CLIENTID",{}'.format(CLIENTID),
    1:'AT+SMCONF="URL",{}'.format(BROKER_IP),
    2:'AT+SMCONF="KEEPTIME",60',
    3:'AT+SMCONF="USERNAME",{}'.format(USERNAME),
    4:'AT+SMCONF"PASSWORD",{}'.format(PASSWORD),
    5:'AT+SMCONF="CLEANSS",0',
    6:'AT+SMCONF="QOS",1',
    7:'AT+SMCONF="TOPIC",{}'.format(TOPIC),
    8:'AT+SMCONF="MESSAGE","Broker Setting"',
    9:'AT+SMCONF="RETAIN",0',
    10:'AT+SMCONN',
}

def create_data():
    Humidity = random.randint(40, 80)
    Temperature = random.randint(20, 80)
    Feature1 = random.randint(1, 100)
    Feature2 = random.randint(1, 100)
    Feature3 = random.randint(1, 100)
    Feature4 = random.randint(1, 100)
    timeString = time.strftime("%Y/%m/%d %H:%M").split(" ")
    data = {
        "_id": 0,
        "DeviceName": "PDMU_1",
        "Humidity": Humidity,
        "Temperature": Temperature,
        "F1": Feature1,
        "F2": Feature2,
        "F3": Feature3,
        "F4": Feature4,
        "Date": timeString[0],
        "Time": timeString[1]
    }
    data = json.dumps(data)
    return data

def mqtt_AutoPub():
    data = create_data()
    print("Data len: {}, \n Data: {}".format(len(data), data))
    command_data = {
        0: 'AT+SMPUB="{}",{},1,1'.format(TOPIC, len(data)),
        1: data
    }
    for i in range(len(command_data)):
        print("---Start Command---\n {}".format(command_data[i]))
        command_storage = (command_data[i]+"\r\n").encode('utf-8')
        serial.write(command_storage)
        sleep(1)
        msg_response = (serial.read(serial.inWaiting())).decode()
        print("Response: {}".format(msg_response.split("\n")))
        print(len(msg_response))
        command_storage=""

if __name__ == "__main__":
    try:
        while True:
            command = input("Please input AT Command\n")
            #Quit console
            if command == "Q":
                print("---Serial Quit---")
                serial.close()
                break
            
            #Auto connect Broker internet
            elif command == "B":
                print("---Serial Auto---")
                for i in range(len(command_brokerSetting)):
                    print(command_brokerSetting[i])
                    print("---Start command : {}---",format(command_brokerSetting[i]))
                    command_storage = (command_brokerSetting[i]+"\r\n").encode('utf-8')
                    serial.write(command_storage)
                    sleep(1)
                    msg_response = (serial.read(serial.inWaiting())).decode()
                    print("Response : {},".format(msg_response.split("\n")))
                    print(len(msg_response))
                    command_storage = ""
                    
            #Initial Setting
            elif command == "I":
                print("---Serial Auto---")
                for i in range(len(command_initial)):
                    print("---Start Command--- \n {}".format(command_initial[i]))
                    command_storage = (command_initial[i]+"\r\n").encode('utf-8')
                    serial.write(command_storage)
                    sleep(1)
                    msg_response = (serial.read(serial.inWaiting())).decode()
                    msg_response = (serial.read(serial.inWaiting())).decode()
                    print("Response : {},".format(msg_response.split("\n")))
                    print(len(msg_response))
                    command_storage = ""
    
            #Send one message
            elif command == "send":
                data = create_data()
                print("Data len: {},\n Data : {} ".format(len(data),data))
                command_data = {
                    0:'AT+SMPUB="test",{},1,1'.format(len(data)),
                    1:data
                }
                for i in range(len(command_data)):
                    print(command_data[i])
                    print("---Start a3e~#E#E3E`command : {}---",format(command_data[i]))
                    command_storage = (command_data[i]+"\r\n").encode('utf-8')
                    serial.write(command_storage)
                    sleep(1)
                    msg_response = (serial.read(serial.inWaiting())).decode()
                    print("Response : {},".format(msg_response.split("\n")))
                    print(len(msg_response))
                    command_storage = ""

            #Send one message
            elif command == "send":
                data = create_data()
                print("Data len: {},\n Data : {} ".format(len(data),data))
                command_data = {
                    0:'AT+SMPUB="test",{},1,1'.format(len(data)),
                    1:data
                }
                for i in range(len(command_data)):
                    print(command_data[i])
                    print("---Start a3e~#E#E3E`command : {}---",format(command_data[i]))
                    command_storage = (command_data[i]+"\r\n").encode('utf-8')
                    serial.write(command_storage)
                    sleep(1)
                    msg_response = (serial.read(serial.inWaiting())).decode()
                    print("Response : {},".format(msg_response.split("\n")))
                    print(len(msg_response))
                    command_storage = ""
                    
            #Around Send
            elif command == "A":
                schedule.every(120).seconds.do(mqtt_AutoPub)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            
            else:
                command = (command + "\r\n").encode('utf-8')
                pub_command = serial.write(command)
                print("Send: ", pub_command)
                sleep
                    
    except Exception as e:
        serial.close()
        print("---Serial Close---")
        print(e)