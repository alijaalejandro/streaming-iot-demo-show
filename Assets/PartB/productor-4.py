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

delivered_records = 0

def job_send_data():
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
    name_object.name = 'galeo-dev-iot-events'
    record_key = name_object.to_dict()
    print(record_key)
    record_value = dict(machineid="15AB45CE",
                        machine_status="normal",
                        machine_critical_stop="no_check",
                        machine_revision="01/05/2020")
    print(record_value)
    print("Producing Avro record: {}\r\n".format(name_object.name))
    p.produce(topic=topic, key=record_key, value=record_value, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush(1)
    print("1 messages were produced to topic {}!\r\n".format(topic))


# Initialization
# Lanzo trabajos y programacion periodica

schedule.every(2).seconds.do(job_send_data)


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
    }, default_key_schema=ccloud_lib.schema_key, default_value_schema=ccloud_lib.schema_value_3)

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)

    while True:
        schedule.run_pending()
        time.sleep(1)