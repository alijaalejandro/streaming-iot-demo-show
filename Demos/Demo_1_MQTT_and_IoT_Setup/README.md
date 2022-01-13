
# Demo 1 Explanation

In this demo we are going to retrieve the sensors' readings from the MQTT topic.

Our lab environment will consist on the following components:

- __Our Raspberry-pi will serve as sensors gateway__. A raspberry-pi is a mini computer Linux-based perfect for testing and experiments. A Raspberry-pi provides a SO interface at the same time that low level access to a micro controller resources like I/O and standard ports for plenty of functionalities.
- A part of the gateway, we are going to use a __couple of digital sensors for rel. humidity and temperature__. We enjoy using real sensors instead of synthetic data due to the lack of their trends and artificial behavior.
- We are going to use a __python script to read data from the sensors using the low level pins of the raspberry pi and pushing this data to the cloud by MQTT protocol.__  

Let's do this step-by-step

0. Check the set up.

By using the remote webcam, we can now check what is in place. Just open the Xiami Mi Home app and access to the video streaming.

 ![Image Webcam](/images/webcam1.PNG)
 ![Image Webcam](/images/webcam2.PNG)


1. MQTT sender and data collection is at the RPI locally at the office.
	Access to the supervisor and check the MQTT sender is up&running
	- To access the supervisor just type this [url](http://agallende.ddns.net:9001/) at the web browser. Enter user & password and get the service running.
	- user and password: ```galeo | G@le0Tech```

	![Image of Supervisor](/images/supervisor.png)

```
2. [DEPRECATED] Connect to the AWS VM. ```ssh -i "GaleoIoTKeys.pem" ubuntu@ec2-3-140-184-237.us-east-2.compute.amazonaws.com```
	- The RPI should send the data over MQTT to an MQTT broker installed into the AWS VM. Please chek the _mosquitto_ process is running at the VM by executing top.
	- Please check the following parameters before proceed ahead
		- VM public IP
		- MQTT standard port is open for allowing traffic (enable a 1883 TCP/IP port general rule at the security config of the. VM)
		- Get the configured broker user and password (```galeo``` ```Hq93*alrEYD98oPT```)
		- Check the broker is running and you are able to connect by using MQTT-Explorer or any other MQTT client.
```

2. In order to get the data from the sensors we are going to use a public cloud MQTT broker hosted by [HiveMQ](https://www.hivemq.com/mqtt-cloud-broker/).
	- HiveMQ has a free MQTT broker cluster available on the web as a complete managed service. 
	- Our broker is listening at this ```1a72e178acf1458a8a6814ac97606398.s2.eu.hivemq.cloud | PORT 8883 (TLS)``` Encryption ready.
	- Here are the details of our cluster
	![HiveMQ Cluster Details](/images/hivemq1.png)
	- Credentials to publish and subscribe are:
	```galeoiot-dev & 3J2Dj3p7kHDz```
	- Check the broker is running and you are able to connect by using MQTT-Explorer or any other MQTT client.
	- Please note that free cluster doesn't have any monitoring console.


3. Get your favorite MQTT client (client or OS native) and configure your broker
	- In this example, we are going to use [MQTT Explorer](http://mqtt-explorer.com/) _Thanks to Thomas Nordquist thomasnordquist_
	- Configure the broker settings:
		- Broker Name
		- Broker url or in our case IP
		- Broker port (default 1883)
		- Broker user & password

![Image of MQTT config](/images/mqttexplorerconfig.png)

4. Access the broker and quick-check the data

![Image of MQTT Data](/images/mqttexplorerdata.png)

5. Activate the smart lamp to force a temperature rising (and the opposite effect in rel. humidity)
 Use the SmartLife App to activate the lamp and check the result in the real time charts at the MQTT client.

 ![Image Lamp](/images/Lamp.PNG)


 6. Bonus Track - Access the Raspberry-pi and look at the code
 ```bash
 	ssh pi@agallende.ddns.net
 	passwd: G@le0Tech
 ```
 ```bash
 	cd class
 	nano sender.py
 ```

 	You can get the code [here](/Assets/raspberry/sender.py) 
 
```python
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
```








