import json
import time
import requests
from kafka import KafkaConsumer
import datetime

HEADERS = {'Content-type': 'application/octet-stream'}
ENDPOINT = "https://api.powerbi.com/beta/fb16d55e-d466-49fc-b4dc-4d5ec301ec20/datasets/b050acea-e026-47a0-809e-41d3e4ed1817/rows?key=YhYjpU4lKaAogeYVE%2FOCFUoZvO30o8dhfuy9z1mxENyUL3ET6aT%2FnvjAmW0P8v5rUwDVSJde6injhvZJfEPZyw%3D%3D"
KAFKA_LOGGER_BOOTSTRAP_SERVERS="pkc-lz6r3.northeurope.azure.confluent.cloud:9092"
KAFKA_LOGGER_TOPIC = 'galeo-dev-iot-alerts'
KAFKA_CLUSTER_API_KEY = "QOWBA2FFPE3RZY5Y"
KAFKA_CLUSTER_API_SECRET = "7sWRXalpEPrVFIxi5LyYdF2dJq6P9Afx0uMiUSy3f1PQNANun8siDNopzNrzqAJs"

def get_kafka_logs():
    """
    Function to retrieve Kafka logs
    """
    consumer = KafkaConsumer(KAFKA_LOGGER_TOPIC,
                             security_protocol="SASL_SSL",
                             bootstrap_servers=[KAFKA_LOGGER_BOOTSTRAP_SERVERS],
                             sasl_mechanism="PLAIN",
                             sasl_plain_username=KAFKA_CLUSTER_API_KEY,
                             sasl_plain_password=KAFKA_CLUSTER_API_SECRET,
                             auto_offset_reset='latest', enable_auto_commit=False)

    # In order to prevent Error 429 for throttling
    while True:
        msgs = consumer.poll(max_records=10, timeout_ms=1000)
        post_messages(msgs)
        time.sleep(1)


def post_messages(messages):
    """
    Recieve a dict of messages and post them to the endpoint
    :param messages: dict
    """
    data = []
    for key, value in messages.items():
        for record in value[:10]:
            json_message = json.loads(record.value)
            o365_datetime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            data.append(
                {
                    "TemperatureValue": json_message.get("TemperatureValue"),
                    "TemperatureThreshold": json_message.get("TemperatureThreshold"),
                    "AlertType": json_message.get("AlertType"),
                    "datetime": o365_datetime
                })
            print(data)
    if len(data) > 0:
        try:
            full_message = json.dumps(data).encode("utf-8")
            result = requests.post(ENDPOINT,
                                   data=full_message,
                                   verify=False,
                                   headers=HEADERS,
                                   stream=True)
            result.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            print(exception)


get_kafka_logs()

