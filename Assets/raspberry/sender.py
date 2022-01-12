import paho.mqtt.client as paho
from paho import mqtt
import time

import RPi.GPIO as GPIO
from pi_sht1x import SHT1x

DATA_PIN = 3
SCK_PIN = 2

temperature_inside = 0
humidity_inside = 0
dew_point_inside = 0
espera = 1

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global espera

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    espera = msg.payload

client = paho.Client()
client.on_publish = on_publish
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("galeoiot-dev", "3J2Dj3p7kHDz")
client.connect("1a72e178acf1458a8a6814ac97606398.s2.eu.hivemq.cloud", 8883)
client.loop_start()

def sensor_inside():
    global temperature_inside, humidity_inside, dew_point_inside

    with SHT1x(DATA_PIN, SCK_PIN, gpio_mode=GPIO.BCM) as sensor:
        temperature_inside = sensor.read_temperature()
        humidity_inside = sensor.read_humidity(temperature_inside)
        dew_point_inside = sensor.calculate_dew_point(temperature_inside, humidity_inside)
        print(temperature_inside, humidity_inside, dew_point_inside)

    print("data_inside complete")

client.on_message = on_message
client.on_subscribe = on_subscribe
client.subscribe("cmdn/sampling", qos=0)


while True:
    sensor_inside()

    (rc, mid) = client.publish("telemetry/temperature_indoor", str(temperature_inside), qos=0)
    (rc, mid) = client.publish("telemetry/humidity_indoor", str(humidity_inside), qos=0)
    (rc, mid) = client.publish("telemetry/dew_point_indoor", str(dew_point_inside), qos=0)

    time.sleep(int(espera))
