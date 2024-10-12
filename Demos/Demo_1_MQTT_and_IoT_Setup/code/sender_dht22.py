import time
import math

import paho.mqtt.client as paho
from paho import mqtt

import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 18

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global espera

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    espera = msg.payload

def calculate_dew_point(temperature, humidity):
    # Constantes empíricas de la fórmula de Magnus-Tetens
    a = 17.27
    b = 237.7
    
    # Calcular alpha(T, RH)
    alpha = (a * temperature) / (b + temperature) + math.log(humidity / 100)
    
    # Calcular el punto de rocío (T_d)
    dew_point = (b * alpha) / (a - alpha)
    
    return round(dew_point, 2)

def sensor_inside():
    global temperature, humidity, dew_point

    # Calibration offsets

    ct = -594.2
    ch = -1324.4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    #temperature_inside = (((temperature_inside_F - 32) / 1.8 ) / 10)
    temperature = temperature + ct
    #temperature = temperature
    humidity = humidity + ch
    dew_point_inside = calculate_dew_point(temperature, humidity)

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%  Dewpoint={0:0.1f}*C'.format(temperature, humidity, dew_point))
    else:
        print('Failed to get reading. Try again!')

    print("data_inside complete")

temperature = 0
humidity = 0
dew_point = 0
espera = 1

client = paho.Client()
client.on_publish = on_publish
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("galeoiot-dev", "3J2Dj3p7kHDz")
client.connect("1a72e178acf1458a8a6814ac97606398.s2.eu.hivemq.cloud", 8883)
client.loop_start()

client.on_message = on_message
client.on_subscribe = on_subscribe
client.subscribe("cmdn/sampling", qos=0)


while True:
    sensor_inside()

    (rc, mid) = client.publish("telemetry/temperature_indoor", str(temperature), qos=0)
    (rc, mid) = client.publish("telemetry/humidity_indoor", str(humidity), qos=0)
    (rc, mid) = client.publish("telemetry/dew_point_indoor", str(dew_point), qos=0)
    
    time.sleep(int(espera))