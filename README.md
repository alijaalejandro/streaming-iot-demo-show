
# Intro

This repo is a kind of hands-on-lab demo lab to test and illustrate some IoT Streaming capabilities.
The repo includes some assets and tools as brick piezes to show some demo use cases. For example:

- A demo [demo1](/Demos/Demo_1_MQTT_and_IoT_Setup) where a set of sensors (temperatue, humidity, etc.) is connected to a __Raspberry Pi (RPI)__. The RPI acts as an IoT Gateway. The sensors' readings are collected and send it by MQTT to a remote broker. Here, we can play with sensors' values, MQTT topics, specific business logic and so on.

- A demo [demo2](/Demos/Demo_2_NodeRED_program) where, starting from this firts set-up (in [demo1](/Demos/Demo_1_MQTT_and_IoT_Setup)) we can develop a simple program in Node-RED to automate and develop some custom logic.

- A demo [demo3](/Demos/Demo_3_MQTT_Confluent_PowerBI) where, starting from [demo2](/Demos/Demo_2_NodeRED_program), once we have the data at the MQTT broker, we can programm a kafka producer and inyect that reading to a Confluent Cloud cluster. From here, we can play a bit with Confluent KQL streaming calculations.

- A demo where [demo3](/Demos/Demo_3_MQTT_Confluent_PowerBI)), starting form Confluent topics, we can programm a simple kafka consumer to get the data and send it to the real-time visualizer in Power BI.  


![Architecture](/images/IoT_Hands-on-lab.jpg)


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

_Note: Students only interact with the demo at the MQTT broker point. The webcam it's just to see the real stuff. The smart lamp can be used during the forums to test programs and business logic. Some of the HW and SW pieces can be used during the course and some others not_

<!--
# Assets and tools

## Sensors readings and MQTT publisher

Sensirion TMP&HR digital sensor connected by private i2c protocol: 2 comms wires + 2 power wires.
(_Optional: Particular Matter sensor connected by serial port with a library._)

The source code for this publisher is in the [raspberry](/Assets/raspberry/sender.py)

You will have to edit the MQTT parameters like:

- Broker IP
- Broker Port: default 8883
- Broker user & passwd
- Enable TLS Encryption


## RPI access

- IP Raspberry: ```gallende.ddns.net``` (ssh port 22)
- Enter user & passwd

## Access to Supervisor utility

The supervisor utility allows us to run process without executing them at the terminal window. Some services like the MQTT publisher is registered in the supervisor list. This means, once we access to the supervisor web interface we can run and stop the service just by clicking one button.

- To access the supervisor just type this [url](http://agallende.ddns.net:9001/) at the web browser. Enter user & password and get the service running.
- Credentials for supervisor are [here](/Credentials/Supervisor_crdentials.json) 

## Access to the actuator

In our case, the simplest actuator is a remote controlled lamp. We have connected a smart plug to our halogen lamp. In this case, the lamp plays the role as an oven or a valve that where it's open the temperature is rising (for example simulating the product flowing through a pipe)

To switch on/off the lamp we must download the Smart Life App and, again, the owner must share the device with our user. After this a new device will appear in the app. Now we are ready to switch on/off the lamp by using the Smart Life app.
_Note: This functionality is restricted to the demo admonostrator and students don't have general access to this asset_
-->


