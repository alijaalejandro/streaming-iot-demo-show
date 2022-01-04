import ssl
import sys

import paho.mqtt.client

from confluent_kafka import Producer, KafkaError
from confluent_kafka.avro import AvroProducer
import json
import ccloud_lib

USER_MQTT = "galeo"
PASSWORD_MQTT = "Hq93*alrEYD98oPT"
TOPIC_MQTT = 'galeo_mqtt'
CLIENT_ID_MQTT = 'galeo-subs'
HOST_MQTT = '127.0.0.1'
PORT_MQTT = 1883


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


def main():
    client = paho.mqtt.client.Client(client_id=CLIENT_ID_MQTT, clean_session=False)
    client.username_pw_set(USER_MQTT, password=PASSWORD_MQTT)  # set username and password
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host=HOST_MQTT, port=PORT_MQTT)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print('connected (%s)\r\n' % client._client_id)
    client.subscribe(topic=TOPIC_MQTT, qos=2)

def on_message(client, userdata, message):
    print('------------------------------\r\n')
    #print('topic_mqtt: %s' % message.topic)
    data_in_json = message.payload
    #print('payload: %s' % data_in_json)
    #print('qos: %d' % message.qos)

    data_in = json.loads(data_in_json)

    def acked(err, msg):
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}\r\n".format(err))
        else:
            print("Produced record to topic {} partition [{}] @ offset {}\r\n"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    record_key = "telemetry"

    if len(data_in) == 14:
        record_value = json.dumps({'temperature_inside': data_in["temperature_inside"],
                                   'humidity_inside': data_in["humidity_inside"],
                                   'dew_point_inside': data_in["dew_point_inside"],
                                   'temperature': data_in["temperature"],
                                   'humidity': data_in["humidity"],
                                   'wind_speed': data_in["wind_speed"],
                                   'uv_index': data_in["uv_index"],
                                   'weather_descriptions': data_in["weather_descriptions"],
                                   'pressure': data_in["pressure"],
                                   'precip': data_in["precip"],
                                   'visibility': data_in["visibility"],
                                   'wind_degree': data_in["wind_degree"],
                                   'feelslike': data_in["feelslike"],
                                   'cloudcover': data_in["cloudcover"]})

        print("Producing record 14: {}\t{}\r\n".format(record_key, record_value))
        p.produce(topic, key=record_key, value=record_value, on_delivery=acked)
        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        p.poll(0)

        p.flush(1)
        print("{} messages were produced to topic {}!\r\n".format(delivered_records, topic))

    else:
        record_value = json.dumps({'temperature': data_in["temperature"],
                                   'humidity': data_in["humidity"],
                                   'wind_speed': data_in["wind_speed"],
                                   'uv_index': data_in["uv_index"],
                                   'weather_descriptions': data_in["weather_descriptions"],
                                   'pressure': data_in["pressure"],
                                   'precip': data_in["precip"],
                                   'visibility': data_in["visibility"],
                                   'wind_degree': data_in["wind_degree"],
                                   'feelslike': data_in["feelslike"],
                                   'cloudcover': data_in["cloudcover"]})

        print("Producing record 11: {}\t{}\r\n".format(record_key, record_value))
        p.produce(topic, key=record_key, value=record_value, on_delivery=acked)
        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        p.poll(0)

        p.flush(1)
        print("{} messages were produced to topic {}!\r\n".format(delivered_records, topic))

main()