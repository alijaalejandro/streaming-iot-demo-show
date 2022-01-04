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

def job_send_data():
    def acked(err, msg):
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))


    record_key = "galeo-dev-iot-events"
    record_value = json.dumps({'machineid': "15AB45CE",
                               'machine_status': "normal",
                               'machine_critical_stop': "no_check"
                               })

    print("Producing record: {}\t{}\r\n".format(record_key, record_value))
    p.produce(topic, key=record_key, value=record_value, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush(1)
    print("{} messages were produced to topic {}!\r\n".format(delivered_records, topic))


# Initialization
# Lanzo trabajos y programacion periodica

schedule.every(3).seconds.do(job_send_data)


if __name__ == '__main__':

    # Initialization
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)

    p = Producer({
        'bootstrap.servers': conf['bootstrap.servers'],
        'sasl.mechanisms': conf['sasl.mechanisms'],
        'security.protocol': conf['security.protocol'],
        'sasl.username': conf['sasl.username'],
        'sasl.password': conf['sasl.password'],
    })

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)

    while True:
        schedule.run_pending()
        time.sleep(1)