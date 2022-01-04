import ssl
import sys

import paho.mqtt.client
import json

from confluent_kafka import Producer, KafkaError
from confluent_kafka.avro import AvroProducer
import json
import ccloud_lib


def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='galeo_mqtt', qos=2)

def on_message(client, userdata, message):
    print('------------------------------')
    print('topic: %s' % message.topic)
    data_in_json = message.payload
    print('payload: %s' % data_in_json)
    print('qos: %d' % message.qos)

    data_in = json.loads(data_in_json)

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
    name_object.name = "telemetry"
    record_key = name_object.to_dict()
    print(record_key)

    if len(data_in) == 14:
        record_value = dict(temperature_inside=data_in["temperature_inside"],
                            humidity_inside=data_in["humidity_inside"],
                            power_inside=data_in["power_inside"],
                            temperature=data_in["temperature"],
                            humidity=data_in["humidity"],
                            wind_speed=data_in["wind_speed"],
                            uv_index=data_in["uv_index"],
                            weather_descriptions=data_in["weather_descriptions"],
                            pressure=data_in["pressure"],
                            precip=data_in["precip"],
                            visibility=data_in["visibility"],
                            wind_degree=data_in["wind_degree"],
                            feelslike=data_in["feelslike"],
                            cloudcover=data_in["cloudcover"])

        print(record_value)
        print("Producing Avro record: {}".format(name_object.name))
        p.produce(topic=topic, key=record_key, value=record_value, on_delivery=acked)

        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        p.poll(0)

        p.flush(1)
        print("1 messages were produced to topic {}!".format(topic))

    else:
        record_value = dict(temperature=data_in["temperature"],
                            humidity=data_in["humidity"],
                            wind_speed=data_in["wind_speed"],
                            uv_index=data_in["uv_index"],
                            weather_descriptions=data_in["weather_descriptions"],
                            pressure=data_in["pressure"],
                            precip=data_in["precip"],
                            visibility=data_in["visibility"],
                            wind_degree=data_in["wind_degree"],
                            feelslike=data_in["feelslike"],
                            cloudcover=data_in["cloudcover"])

        print(record_value)
        print("Producing Avro record: {}".format(name_object.name))
        p_11.produce(topic=topic, key=record_key, value=record_value, on_delivery=acked)

        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        p_11.poll(0)

        p_11.flush(1)
        print("1 messages were produced to topic {}!".format(topic))

user="galeo"

def main():
    client = paho.mqtt.client.Client(client_id='galeo-subs', clean_session=False)
    client.username_pw_set(user, password="Hq93*alrEYD98oPT")  # set username and password
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='127.0.0.1', port=1883)
    client.loop_forever()

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

    p_11 = AvroProducer({
        'bootstrap.servers': conf['bootstrap.servers'],
        'sasl.mechanisms': conf['sasl.mechanisms'],
        'security.protocol': conf['security.protocol'],
        'sasl.username': conf['sasl.username'],
        'sasl.password': conf['sasl.password'],
        'schema.registry.url': conf['schema.registry.url'],
        'schema.registry.basic.auth.credentials.source': conf['basic.auth.credentials.source'],
        'schema.registry.basic.auth.user.info': conf['schema.registry.basic.auth.user.info']
    }, default_key_schema=ccloud_lib.schema_key, default_value_schema=ccloud_lib.schema_value_11)

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)

    main()

sys.exit(0)