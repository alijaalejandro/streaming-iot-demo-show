import json
import time
import requests
from kafka import KafkaConsumer
import datetime
import paho.mqtt.client as paho

# Config MQTT
broker="192.168.2.23"
port=1883

def on_publish(client,userdata,result):              #create function for callback
    #print("data published \n")
    pass

client1= paho.Client("PC-Confluent")                           #create client object
client1.on_publish = on_publish
client1.connect(broker,port)                         #establish connection

HEADERS = {'Content-type': 'application/octet-stream'}
KAFKA_LOGGER_BOOTSTRAP_SERVERS="pkc-lgwgm.eastus2.azure.confluent.cloud:9092"
KAFKA_LOGGER_TOPIC = 'galeo-dev-iot-rechargepoint-state'
KAFKA_LOGGER_TOPIC2 = 'galeo-dev-iot-rechargepoint-telemetry'
KAFKA_LOGGER_TOPIC3 = 'galeo-dev-iot-rechargepoint-command'
KAFKA_CLUSTER_API_KEY = "4IDQNOEJ7HGPFPTR"
KAFKA_CLUSTER_API_SECRET = "4MfAh0lkss7etGZir+5g+MRWdjo957w6iWgY+9CmQVD+6K53n144lioZ5dJPSDs7"

topic3_data = {'Power_Phase1_Max_Outlet1': 0, 'Power_Phase2_Max_Outlet1': 0, 'Power_Phase3_Max_Outlet1': 0, 'Power_Phase1_Max_Outlet2': 0, 'Power_Phase2_Max_Outlet2': 0, 'Power_Phase3_Max_Outlet2': 0, 'Power_Phase1_Total_Max': 0, 'Power_Phase2_Total_Max': 0, 'Power_Phase3_Total_Max': 0}

def get_kafka_logs():
    """
    Function to retrieve Kafka logs
    """
    consumer3 = KafkaConsumer(KAFKA_LOGGER_TOPIC3,
                             security_protocol="SASL_SSL",
                             bootstrap_servers=[KAFKA_LOGGER_BOOTSTRAP_SERVERS],
                             sasl_mechanism="PLAIN",
                             sasl_plain_username=KAFKA_CLUSTER_API_KEY,
                             sasl_plain_password=KAFKA_CLUSTER_API_SECRET,
                             auto_offset_reset='lastest', enable_auto_commit=False)

    # In order to prevent Error 429 for throttling
    msgs3_old = 0

    while True:
        msgs3 = consumer3.poll(max_records=1, timeout_ms=1000)
        print(msgs3)
        if msgs3_old != msgs3:
            post_messages(msgs3)

        time.sleep(1)


def post_messages(messages3):
    """
    Recieve a dict of messages and post them to the endpoint
    :param messages: dict
    """
    global topic3_data

    for key, value in messages3.items():
        for record in value[:10]:
            json_message3 = json.loads(record.value)

            '''
            topic3_data.update({'Power_Phase1_Max_Outlet1':json_message3.get("Power_Phase1_Max_Outlet1")})
            topic3_data.update({'Power_Phase2_Max_Outlet1':json_message3.get("Power_Phase2_Max_Outlet1")})
            topic3_data.update({'Power_Phase3_Max_Outlet1':json_message3.get("Power_Phase3_Max_Outlet1")})
            topic3_data.update({'Power_Phase1_Max_Outlet2':json_message3.get("Power_Phase1_Max_Outlet2")})
            topic3_data.update({'Power_Phase2_Max_Outlet2':json_message3.get("Power_Phase2_Max_Outlet2")})
            topic3_data.update({'Power_Phase3_Max_Outlet2':json_message3.get("Power_Phase3_Max_Outlet2")})
            topic3_data.update({'Power_Phase1_Total_Max':json_message3.get("Power_Phase1_Total_Max")})
            topic3_data.update({'Power_Phase2_Total_Max':json_message3.get("Power_Phase2_Total_Max")})
            topic3_data.update({'Power_Phase3_Total_Max':json_message3.get("Power_Phase3_Total_Max")})
            '''
            ret= client1.publish("Power_Phase1_Max_Outlet1", json_message3.get("Power_Phase1_Max_Outlet1"))
            ret= client1.publish("Power_Phase2_Max_Outlet1", json_message3.get("Power_Phase2_Max_Outlet1"))
            ret= client1.publish("Power_Phase3_Max_Outlet1", json_message3.get("Power_Phase3_Max_Outlet1"))
            ret= client1.publish("Power_Phase1_Max_Outlet2", json_message3.get("Power_Phase1_Max_Outlet2"))
            ret= client1.publish("Power_Phase2_Max_Outlet2", json_message3.get("Power_Phase2_Max_Outlet2"))
            ret= client1.publish("Power_Phase3_Max_Outlet2", json_message3.get("Power_Phase3_Max_Outlet2"))
            ret= client1.publish("Power_Phase1_Total_Max", json_message3.get("Power_Phase1_Total_Max"))
            ret= client1.publish("Power_Phase2_Total_Max", json_message3.get("Power_Phase2_Total_Max"))
            ret= client1.publish("Power_Phase3_Total_Max", json_message3.get("Power_Phase3_Total_Max"))

            #print(topic3_data)

get_kafka_logs()

