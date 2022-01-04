from json import loads
import time
import requests
from kafka import KafkaConsumer
import datetime
import paho.mqtt.client as paho

# Config MQTT
broker="192.168.2.23"
port=1883

def on_publish(client,userdata,result):              #create function for callback
    print("data published \n")
    pass

client1= paho.Client("PC-Confluent")                           #create client object
client1.on_publish = on_publish
client1.connect(broker,port)

# Config Kafka
HEADERS = {'Content-type': 'application/octet-stream'}
KAFKA_LOGGER_BOOTSTRAP_SERVERS="pkc-lgwgm.eastus2.azure.confluent.cloud:9092"
#KAFKA_LOGGER_TOPIC = 'galeo-dev-iot-rechargepoint-command'
KAFKA_LOGGER_TOPIC = 'verde'
KAFKA_CLUSTER_API_KEY = "4IDQNOEJ7HGPFPTR"
KAFKA_CLUSTER_API_SECRET = "4MfAh0lkss7etGZir+5g+MRWdjo957w6iWgY+9CmQVD+6K53n144lioZ5dJPSDs7"

## Retrieve data from kafka (WHAT ABOUT MISSED MESSAGES?)

consumer = KafkaConsumer(KAFKA_LOGGER_TOPIC,
	                         security_protocol="SASL_SSL",
	                         bootstrap_servers=[KAFKA_LOGGER_BOOTSTRAP_SERVERS],
	                         sasl_mechanism="PLAIN",
	                         sasl_plain_username=KAFKA_CLUSTER_API_KEY,
	                         sasl_plain_password=KAFKA_CLUSTER_API_SECRET,
	                         auto_offset_reset='earliest', enable_auto_commit=True,
	                         auto_commit_interval_ms=1000)

# Send data
for message in consumer:
    message = loads(message.value.decode('utf-8'))
    print(message)
    client1.publish("Power_Phase1_Max_Outlet1_write", int(message.get("Power_Phase1_Max_Outlet1")))
    client1.publish("Power_Phase2_Max_Outlet1_write", message.get("Power_Phase2_Max_Outlet1"))
    client1.publish("Power_Phase3_Max_Outlet1_write", message.get("Power_Phase3_Max_Outlet1"))
    client1.publish("Power_Phase1_Max_Outlet2_write", message.get("Power_Phase1_Max_Outlet2"))
    client1.publish("Power_Phase2_Max_Outlet2_write", message.get("Power_Phase2_Max_Outlet2"))
    client1.publish("Power_Phase3_Max_Outlet2_write", message.get("Power_Phase3_Max_Outlet2"))
    client1.publish("Power_Phase1_Total_Max_write", message.get("Power_Phase1_Total_Max"))
    client1.publish("Power_Phase2_Total_Max_write", message.get("Power_Phase2_Total_Max"))
    client1.publish("Power_Phase3_Total_Max_write", message.get("Power_Phase3_Total_Max"))
