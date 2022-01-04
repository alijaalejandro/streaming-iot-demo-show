
# Intro

This repo is a kind of hands-on-lab demo lab to test and illustrate some IoT Streaming capabilities.
The repo includes some assets and tools as brick piezes to show some demo use cases. For example:

- A demo [demo1](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Demos/Demo-1-%20MQTT%20and%20IoT%20Setup/) where a set of sensors (temperatue, humidity, etc.) is connected to a Raspberry Pi (RPI). The RPI acts as an IoT Gateway. The sensors' readings are collected and send it by MQTT to a remote broker. Here, we can play with sensors' values, MQTT topics, specific business logic and so on.

- A demo [demo2](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Demos/Demo-2%20-%20NodeRED%20program/) where, starting from the firts set-up we can develop a simple program in Node-RED to automate and develop some custom logic.

- A demo [demo3](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Demos/Demo-3%20-%20MQTT-Confluent-PowerBI/) where, starting from the firts demo, once we have the data at the MQTT broker, we can programm a kafka producer and inyect that reading to a Confluent infra. From here, we can play a bit with Confluent KQL streaming calculations.

- A demo where [demo3](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Demos/Demo-3%20-%20MQTT-Confluent-PowerBI/), starting form Confluent topics, we can programm a simple kafka consumer to get the data and send it to the real-time visualizer in Power BI.  


# Demo components

* Hardware

	- Raspberry pi 3 - Raspberry PI OS lite 2020
	- Sensors:
		- TMP&HR and Dwe point - SHT75 Sensirion
		- PM in air - PMS5003
	- Smart Switch  TECKIN SP21
	- Web Cam Creative VF0770

* Software

	- RPI SO: Raspberry PI OS lite 2020
	- MQTT Broker - Mosquitto
	- VM Linux Ubuntu en AWS
	- Confluent Cloud
	- MQTT mobile client apps
	- Smart Switch iOS App

# Assets and tools

## Sensors readings and MQTT publisher

Sensirion TMP&HR digital sensor connected by private i2c protocol: 2 comms wires + 2 power wires.
Particular Matter sensor connected by serial port with a library.

The source code for this publisher is in the [raspberry](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Assets/raspberry/) folder within the [asset](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Assets/) folder.

You will have to edit the MQTT parameters like:

- Broker IP
- Broker Port: default 1883
- Broker user & passwd


## RPI access

- IP Raspberry: Adrian's Public IP TBD (ssh port 22)
- Enter user & passwd

## Access to Supervisor utility

The supervisor utility allows us to run process without executing them at the terminal window. Some services like the MQTT publisher is registered in the supervisor list. This means, once we access to the supervisor web interface we can run and stop the service just by clicking one button.

To acces the supervisor just type this [url](http://77.231.175.157:9001/) at the web browser. Enter user & passwd and get the service running. 



## Take a visual of the set-up

The RPI and sensors are set it up in a remote, undisclosed location. To have a visual of what is happpening there we have enabled a web cam with a remote access.
Webcam is accessible throught:

We need to download the Xiaomi MI Home. Then, the webcam owner must share the device with our user. After this a new device will appear in the app. Now we are ready to see the video streaming.


## Get measuremnts from the MQTT Broker.

The MQTT broker has been installed at the AWS Virtual Machine
The VM is running a Ubuntu Linux distro.
The MQTT broker is the standard version of the [Mosquitto](https://mosquitto.org/)

## Access to the actuator

In our case, the simplest actuator is a remote controlled lamp. We have connected a smart plug to our halogen lamp. In this case, the lamp plays the role as an oven or a valve that where it's open the temperature is rising (for example simulating the product flowing through a pipe)

To switch on/off the lamp we must download the Samrt Life App and, again, the owner must share the device with our user. After this a new device will appear in the app. Now we are ready to switch on/off the lamp by using the Smart Life app.


