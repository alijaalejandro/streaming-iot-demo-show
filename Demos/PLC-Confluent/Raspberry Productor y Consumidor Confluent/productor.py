# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Envio de telemetria
#
# =============================================================================

# coding: utf-8
import time
import requests
import random

from confluent_kafka import Producer, KafkaError
import json
import ccloud_lib

import paho.mqtt.client as paho
import Queue

# Config MQTT
broker="192.168.2.23"
port=1883

def on_message(client, userdata, message):
   q.put(message)

client1= paho.Client("PC-Confluent")                           #create client object
client1.connect(broker,port)                         #establish connection
client1.on_message = on_message
client1.subscribe("#")
client1.loop_start()

q = Queue.Queue()

# Variables
delivered_records = 0
delivered_records2 = 0
delivered_records3 = 0
topic_data = {'FSM_State_Outlet1': 0, 'FSM_State_Outlet2': 0, 'Number_Available_CPs': 0}
topic2_data = {'Power_Outlet1': 0, 'Power_Outlet2': 0, 'Energy_Outlet1': 0, 'Energy_Outlet2': 0}
topic3_data = {'Power_Phase1_Total': 0, 'Power_Phase2_Total': 0, 'Power_Phase3_Total': 0, 'Power_Phase1_Max_Outlet1': 0, 'Power_Phase2_Max_Outlet1': 0, 'Power_Phase3_Max_Outlet1': 0, 'Power_Phase1_Max_Outlet2': 0, 'Power_Phase2_Max_Outlet2': 0, 'Power_Phase3_Max_Outlet2': 0, 'Power_Phase1_Total_Max': 0, 'Power_Phase2_Total_Max': 0, 'Power_Phase3_Total_Max': 0}

# Configuracion Topics
topic = "galeo-dev-iot-rechargepoint-state"
topic2 = "galeo-dev-iot-rechargepoint-telemetry"
#topic3 = "galeo-dev-iot-rechargepoint-command"
topic3 = "verde"


def job_send_data():
    global topic_data

    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}\r\n".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}\r\n"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    record_key = "galeo-dev-iot-rechargepoint-state"
    record_value = json.dumps({'FSM_State_Outlet1': topic_data.get('FSM_State_Outlet1'),
                               'FSM_State_Outlet2': topic_data.get('FSM_State_Outlet2'),
                               'Number_Available_CPs': topic_data.get('Number_Available_CPs')})

    print("Producing record: {}\t{}\r\n".format(record_key, record_value))
    p.produce(topic, key=record_key, value=record_value, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush()
    print("{} messages were produced to topic {}!\r\n".format(delivered_records, topic))


def job_send_data2():
    global topic2_data

    def acked(err, msg):
        global delivered_records2
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}\r\n".format(err))
        else:
            delivered_records2 += 1
            print("Produced record to topic {} partition [{}] @ offset {}\r\n"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    record_key2 = "galeo-dev-iot-rechargepoint-telemetry"
    record_value2 = json.dumps({'Power_Outlet1': topic2_data.get('Power_Outlet1'),
                                'Power_Outlet2': topic2_data.get('Power_Outlet2'),
                                'Energy_Outlet1': topic2_data.get('Energy_Outlet1'),
                                'Energy_Outlet2': topic2_data.get('Energy_Outlet2')})

    print("Producing record: {}\t{}\r\n".format(record_key2, record_value2))
    p.produce(topic2, key=record_key2, value=record_value2, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush()
    print("{} messages were produced to topic {}!\r\n".format(delivered_records2, topic2))

def job_send_data3():
    global topic3_data

    def acked(err, msg):
        global delivered_records3
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}\r\n".format(err))
        else:
            delivered_records3 += 1
            print("Produced record to topic {} partition [{}] @ offset {}\r\n"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    #record_key3 = "galeo-dev-iot-rechargepoint-comands"
    record_key3 = "verde"
    record_value3 = json.dumps({'Power_Phase1_Total': topic3_data.get('Power_Phase1_Total'),
                                'Power_Phase2_Total': topic3_data.get('Power_Phase2_Total'),
                                'Power_Phase3_Total': topic3_data.get('Power_Phase3_Total'),
                                'Power_Phase1_Max_Outlet1': topic3_data.get('Power_Phase1_Max_Outlet1'),
                                'Power_Phase2_Max_Outlet1': topic3_data.get('Power_Phase2_Max_Outlet1'),
                                'Power_Phase3_Max_Outlet1': topic3_data.get('Power_Phase3_Max_Outlet1'),
                                'Power_Phase1_Max_Outlet2': topic3_data.get('Power_Phase1_Max_Outlet2'),
                                'Power_Phase2_Max_Outlet2': topic3_data.get('Power_Phase2_Max_Outlet2'),
                                'Power_Phase3_Max_Outlet2': topic3_data.get('Power_Phase3_Max_Outlet2'),
                                'Power_Phase1_Total_Max': topic3_data.get('Power_Phase1_Total_Max'),
                                'Power_Phase2_Total_Max': topic3_data.get('Power_Phase2_Total_Max'),
                                'Power_Phase3_Total_Max': topic3_data.get('Power_Phase3_Total_Max')})

    print("Producing record: {}\t{}\r\n".format(record_key3, record_value3))
    p.produce(topic3, key=record_key3, value=record_value3, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush()
    print("{} messages were produced to topic {}!\r\n".format(delivered_records3, topic3))

if __name__ == '__main__':
    # Initialization Confluent
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)

    # Create Producer instance
    p = Producer({
        'bootstrap.servers': conf['bootstrap.servers'],
        'sasl.mechanisms': conf['sasl.mechanisms'],
        'security.protocol': conf['security.protocol'],
        'sasl.username': conf['sasl.username'],
        'sasl.password': conf['sasl.password'],
    })

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)
    ccloud_lib.create_topic(conf, topic2)
    ccloud_lib.create_topic(conf, topic3)

    while True:
        flag1 = 0
        flag2 = 0
        flag3 = 0
        
        while not q.empty():
            message = q.get()

            if message is None:
                continue
            else:
                if message.topic == "FSM_State_Outlet1":
                    topic_data.update({"FSM_State_Outlet1": int(message.payload.decode("utf-8"))})
                    flag1 = 1
                if message.topic == "FSM_State_Outlet2":
                    topic_data.update({"FSM_State_Outlet2": int(message.payload.decode("utf-8"))})
                    flag1 = 1
                if message.topic == "Number_Available_CPs":
                    topic_data.update({"Number_Available_CPs": int(message.payload.decode("utf-8"))})
                    flag1 = 1

                if message.topic == "Power_Outlet1":
                    topic2_data.update({"Power_Outlet1": int(message.payload.decode("utf-8"))})
                    flag2 = 1
                if message.topic == "Power_Outlet2":
                    topic2_data.update({"Power_Outlet2": int(message.payload.decode("utf-8"))})
                    flag2 = 1
                if message.topic == "Energy_Outlet1":
                    topic2_data.update({"Energy_Outlet1": int(message.payload.decode("utf-8"))})
                    flag2 = 1
                if message.topic == "Energy_Outlet2":
                    topic2_data.update({"Energy_Outlet2": int(message.payload.decode("utf-8"))})
                    flag2 = 1

                if message.topic == "Power_Phase1_Total":
                    topic3_data.update({"Power_Phase1_Total": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase2_Total":
                    topic3_data.update({"Power_Phase2_Total": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase3_Total":
                    topic3_data.update({"Power_Phase3_Total": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase1_Max_Outlet1":
                    topic3_data.update({"Power_Phase1_Max_Outlet1": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase2_Max_Outlet1":
                    topic3_data.update({"Power_Phase2_Max_Outlet1": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase3_Max_Outlet1":
                    topic3_data.update({"Power_Phase3_Max_Outlet1": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase1_Max_Outlet2":
                    topic3_data.update({"Power_Phase1_Max_Outlet2": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase2_Max_Outlet2":
                    topic3_data.update({"Power_Phase2_Max_Outlet2": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase3_Max_Outlet2":
                    topic3_data.update({"Power_Phase3_Max_Outlet2": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase1_Total_Max":
                    topic3_data.update({"Power_Phase1_Total_Max": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase2_Total_Max":
                    topic3_data.update({"Power_Phase2_Total_Max": int(message.payload.decode("utf-8"))})
                    flag3 = 1
                if message.topic == "Power_Phase3_Total_Max":
                    topic3_data.update({"Power_Phase3_Total_Max": int(message.payload.decode("utf-8"))})
                    flag3 = 1

        if flag1 == 1:
            print("JOB 1")
            job_send_data()
            flag1 = 0
        if flag2 == 1:
            print("JOB 2")
            job_send_data2()
            flag2 = 0
        if flag3 == 1:
            print("JOB 3")
            job_send_data3()
            flag3 = 0


