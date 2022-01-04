import time
import RPi.GPIO as GPIO
from pi_sht1x import SHT1x

import paho.mqtt.client as mqttClient
import time

import schedule
import requests
import random

import json
import sys

DATA_PIN = 3
SCK_PIN = 2

temperature_inside = 0
humidity_inside = 0
dew_point_inside = 0

def job_sensor_outside():
    api_result = requests.get('http://api.weatherstack.com/current',
                              params={'access_key': '0689083ffc61441218fc05cf31c312d8', 'query': 'Gijon'},)
    api_response = api_result.json()

    print("data_outside complete")
    return api_response

def job_sensor_inside():
    global temperature_inside, humidity_inside, dew_point_inside

    with SHT1x(DATA_PIN, SCK_PIN, gpio_mode=GPIO.BCM) as sensor:
        temperature_inside = sensor.read_temperature()
        humidity_inside = sensor.read_humidity(temperature_inside)
        dew_point_inside = sensor.calculate_dew_point(temperature_inside, humidity_inside)
        print(temperature_inside, humidity_inside, dew_point_inside)

    print("data_inside complete")

def job_send_data(api_response):
    global temperature_inside, humidity_inside, dew_point_inside

    if(sys.argv[1]) == '1':
        data_out = json.dumps({"temperature": api_response['current']['temperature'],
                               "humidity": api_response['current']['humidity'],
                               "wind_speed": api_response['current']['wind_speed'],
                               "uv_index": api_response['current']['uv_index'],
                               "weather_descriptions": 0,
                               "pressure": api_response['current']['pressure'],
                               "precip": api_response['current']['precip'],
                               "visibility": api_response['current']['visibility'],
                               "wind_degree": api_response['current']['wind_degree'],
                               "feelslike": api_response['current']['feelslike'],
                               "cloudcover": api_response['current']['cloudcover']});
    else:
        data_out = json.dumps({"temperature_inside": temperature_inside,
                               "humidity_inside": humidity_inside,
                               "dew_point_inside": dew_point_inside,
                               "temperature": api_response['current']['temperature'],
                               "humidity": api_response['current']['humidity'],
                               "wind_speed": api_response['current']['wind_speed'],
                               "uv_index": api_response['current']['uv_index'],
                               "weather_descriptions": 0,
                               "pressure": api_response['current']['pressure'],
                               "precip": api_response['current']['precip'],
                               "visibility": api_response['current']['visibility'],
                               "wind_degree": api_response['current']['wind_degree'],
                               "feelslike": api_response['current']['feelslike'],
                               "cloudcover": api_response['current']['cloudcover']});

    client.publish(sys.argv[2], data_out)
    print("MQTT send")


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:

        print("Connection failed")


Connected = False  # global variable for the state of the connection

broker_address = "18.224.3.98"
port = 1883
user = "galeo"

client = mqttClient.Client("Raspberry")  # create new instance
client.username_pw_set(user, password="Hq93*alrEYD98oPT")  # set username and password
client.on_connect = on_connect  # attach function to callback
client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop

while Connected != True:  # Wait for connection
    time.sleep(0.1)

# Initialization
api_result = requests.get('http://api.weatherstack.com/current',
                          params={'access_key': '0689083ffc61441218fc05cf31c312d8', 'query': 'Gijon'}, )
api_response = api_result.json()

# Lanzo trabajos y programacion periodica
job_sensor_outside()
job_sensor_inside()

schedule.every(1).hours.do(job_sensor_outside)
schedule.every(10).seconds.do(job_sensor_inside)
schedule.every(10).seconds.do(job_send_data, api_response=api_response)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:

    client.disconnect()
    client.loop_stop()