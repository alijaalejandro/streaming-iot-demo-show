import time
import math

import paho.mqtt.client as paho
from paho import mqtt

import board
import adafruit_dht

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
    global temperature_inside, humidity_inside, dew_point_inside

    with adafruit_dht.DHT22(board.D24, use_pulseio=False) as dhtDevice:
        temperature_c = dhtDevice.temperature
        temperature_inside = temperature_c * (9 / 5) + 32
        humidity_inside = dhtDevice.humidity

        temperature_inside = sensor.read_temperature()
        humidity_inside = sensor.read_humidity(temperature_inside)
        dew_point_inside = calculate_dew_point(temperature_inside, humidity_inside)
        print(temperature_inside, humidity_inside, dew_point_inside)

    print("data_inside complete")

temperature_inside = 0
humidity_inside = 0
dew_point_inside = 0
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
    try:
        sensor_inside()

        (rc, mid) = client.publish("telemetry/temperature_indoor", str(temperature_inside), qos=0)
        (rc, mid) = client.publish("telemetry/humidity_indoor", str(humidity_inside), qos=0)
        (rc, mid) = client.publish("telemetry/dew_point_indoor", str(dew_point_inside), qos=0)
    
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    
    time.sleep(int(espera))
