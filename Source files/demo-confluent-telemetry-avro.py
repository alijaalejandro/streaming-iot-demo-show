#!/usr/bin/env python

# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Writes Avro data, integration with Confluent Cloud Schema Registry
# Envio datos telemetria
#
# =============================================================================

import schedule
import time
import requests
import random

from confluent_kafka import Producer, KafkaError
from confluent_kafka.avro import AvroProducer
import json
import ccloud_lib

temperature_inside = 0
humidity_inside = 0
power_inside = 0
delivered_records = 0

def job_sensor_outside():
    api_result = requests.get('http://api.weatherstack.com/current',
                              params={'access_key': '0689083ffc61441218fc05cf31c312d8', 'query': 'Gijon'},)
    api_response = api_result.json()

    print("data_outside complete")
    return api_response

def job_sensor_inside():
    global temperature_inside, humidity_inside, power_inside

    temperature_inside = random.randint(20,40)
    humidity_inside = random.randint(0,100)
    power_inside = random.randint(0,100)

    print("data_inside complete")

def job_send_data(api_response):
    global temperature_inside, humidity_inside, power_inside

    def acked(err, msg):
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    name_object = ccloud_lib.Name()
    name_object.name = 'telemtry'
    record_key = name_object.to_dict()
    print(record_key)
    record_value = dict(temperature_inside=temperature_inside,
                        humidity_inside=humidity_inside,
                        power_inside=power_inside,
                        temperature=api_response['current']['temperature'],
                        humidity=api_response['current']['humidity'],
                        wind_speed=api_response['current']['wind_speed'],
                        uv_index=api_response['current']['uv_index'],
                        weather_descriptions=0,
                        pressure=api_response['current']['pressure'],
                        precip=api_response['current']['precip'],
                        visibility=api_response['current']['visibility'],
                        wind_degree=api_response['current']['wind_degree'],
                        feelslike=api_response['current']['feelslike'],
                        cloudcover=api_response['current']['cloudcover'])
    print(record_value)
    print("Producing Avro record: {}".format(name_object.name))
    p.produce(topic=topic, key=record_key, value=record_value, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush(1)
    print("10 messages were produced to topic {}!".format(topic))


# Initialization
api_result = requests.get('http://api.weatherstack.com/current',
                          params={'access_key': '0689083ffc61441218fc05cf31c312d8', 'query': 'Gijon'}, )
api_response = api_result.json()

# Lanzo trabajos y programacion periodica
job_sensor_outside()
job_sensor_inside()

schedule.every(1).hours.do(job_sensor_outside)
schedule.every(5).seconds.do(job_sensor_inside)
schedule.every(5).seconds.do(job_send_data, api_response=api_response)


if __name__ == '__main__':

    # Initialization
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)
    # Create AvroProducer instance
    p = AvroProducer({
        'bootstrap.servers': conf['bootstrap.servers'],
        'sasl.mechanisms': conf['sasl.mechanisms'],
        'security.protocol': conf['security.protocol'],
        'sasl.username': conf['sasl.username'],
        'sasl.password': conf['sasl.password'],
        'schema.registry.url': conf['schema.registry.url'],
        'schema.registry.basic.auth.credentials.source': conf['basic.auth.credentials.source'],
        'schema.registry.basic.auth.user.info': conf['schema.registry.basic.auth.user.info'] 
    }, default_key_schema=ccloud_lib.schema_key, default_value_schema=ccloud_lib.schema_value)

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)

    while True:
        schedule.run_pending()
        time.sleep(1)