import time
import module_openmeteo

import paho.mqtt.client as paho
from paho import mqtt

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global espera

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    espera = msg.payload

def sensor_inside(df, reg):
    global temperature_inside, humidity_inside, dew_point_inside

    temperature_inside = df.iloc[reg]["temperature_2m"]
    humidity_inside  = df.iloc[reg]["relative_humidity_2m"]
    dew_point_inside  = df.iloc[reg]["dew_point_2m"]
    
    print(temperature_inside, humidity_inside, dew_point_inside)
    print("data_inside complete")

temperature_inside = 0
humidity_inside = 0
dew_point_inside = 0
espera = 1
reg = 0

# Calculo el número de registros descargados
df = module_openmeteo.get_data_meteo(25.0772, 55.3093, "2025-01-01", "2025-02-01")
num_reg = df.shape[0]

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
        reg = reg + 1
        if reg > num_reg:
            reg = 0
        sensor_inside(df, reg)

        (rc, mid) = client.publish("telemetry/temperature_indoor", str(temperature_inside), qos=0)
        (rc, mid) = client.publish("telemetry/humidity_indoor", str(humidity_inside), qos=0)
        (rc, mid) = client.publish("telemetry/dew_point_indoor", str(dew_point_inside), qos=0)
    
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        raise error
    
    time.sleep(int(espera))