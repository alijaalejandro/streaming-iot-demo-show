# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
# Envio de telemetria
#
# =============================================================================

# coding: utf-8
import schedule
import time
import requests
import random

from confluent_kafka import Producer, KafkaError
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

    print("data_outside complete\r\n")
    return api_response

def job_sensor_inside():
    global temperature_inside, humidity_inside, power_inside

    temperature_inside = random.randint(20,40)
    humidity_inside = random.randint(0,100)
    power_inside = random.randint(0,100)

    print("data_inside complete\r\n")

def job_send_data(api_response):
    global temperature_inside, humidity_inside, power_inside

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

    record_key = "galeo-dev-iot-telemetry"
    record_value = json.dumps({'temperature': api_response['current']['temperature'],
                               'humidity': api_response['current']['humidity'],
                               'wind_speed': api_response['current']['wind_speed'],
                               'uv_index': api_response['current']['uv_index'],
                               'weather_descriptions': 0,
                               'pressure': api_response['current']['pressure'],
                               'precip': api_response['current']['precip'],
                               'visibility': api_response['current']['visibility'],
                               'wind_degree': api_response['current']['wind_degree'],
                               'feelslike': api_response['current']['feelslike'],
                               'cloudcover': api_response['current']['cloudcover']})

    print("Producing record: {}\t{}\r\n".format(record_key, record_value))
    p.produce(topic, key=record_key, value=record_value, on_delivery=acked)
    # p.poll() serves delivery reports (on_delivery)
    # from previous produce() calls.
    p.poll(0)

    p.flush(1)
    print("{} messages were produced to topic {}!\r\n".format(delivered_records, topic))


# Initialization
api_result = requests.get('http://api.weatherstack.com/current',
                          params={'access_key': '0689083ffc61441218fc05cf31c312d8', 'query': 'Gijon'}, )
api_response = api_result.json()

# Lanzo trabajos y programacion periodica
job_sensor_outside()
job_sensor_inside()

schedule.every(1).hours.do(job_sensor_outside)
schedule.every(3).seconds.do(job_sensor_inside)
schedule.every(3).seconds.do(job_send_data, api_response=api_response)


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

    while True:
        schedule.run_pending()
        time.sleep(1)
