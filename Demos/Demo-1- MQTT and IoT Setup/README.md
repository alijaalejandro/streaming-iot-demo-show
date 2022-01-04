
# Demo 1 Explanation

In this demo we are going to retrieve the sensors' readinngs from the MQTT topic.

Our lab environment will consist on the following components:

- Our Raspberrypi will serve as sensors gateway. A raspberrypi is a mini computer Linux-based perfect for testing and experiments. A Raspberrypi provides a SO interface at the same time that low level accces to a microcontroller resources like I/O and estandar ports for plenty of functionalities.
- A part of the gateway, we are going to use a couple of digital sensors for rel. humidity and temperature. We enjoy using real sensors instead of synthetic data due to the lack of their trends and artificial behaviour.
- We are going to use a python script to read data from the sensors using the low level pins of the raspberrypi and pushing this data to the cloud by MQTT protocol.  

Let's do this step-by-step

0. Check the set up.

By using the remote webcam, we can now check what is in place. Just open the Xiami Mi Home app and acces to the video streaming.

 ![Image Webcam](/images/webcam1.PNG)
 ![Image Webcam](/images/webcam2.PNG)


1. MQTT sender and data collection is at the RPI locally at Adrian's houses.
	Acces to the supervisor and check the MQTT sender is up&running
	- To acces the supervisor just type this [url](http://77.231.175.157:9001/) at the web browser. Enter user & passwd and get the service running. 
	![Image of Supervisor](/images/supervisor.png)

```
2. [DEPRECATED] Connect to the AWS VM. ```ssh -i "GaleoIoTKeys.pem" ubuntu@ec2-3-140-184-237.us-east-2.compute.amazonaws.com```
	- The RPI should send the data over MQTT to an MQTT broker installed into the AWS VM. Please chek the _mosquitto_ process is running at the VM by executing top.
	- Please check the following parameters before proceed ahead
		- VM public IP
		- MQTT standart port is open for allowing traffic (enable a 1883 TCP/IP port general rule at the security config of the. VM)
		- Get the configured broker user and passwd (```galeo``` ```Hq93*alrEYD98oPT```)
		- Check the broker is running and you are able to connect by using MQTT-Explorer or any other MQTT client.
```

2. In order to get the data from the sensors we are going to use a public cloud MQTT broker hosted by [HiveMQ](https://www.hivemq.com/mqtt-cloud-broker/).
	- HiveMQ has a free MQTT broket cluster available on the web as a complete managed service. 
	- Our broker is listening at this ```1a72e178acf1458a8a6814ac97606398.s2.eu.hivemq.cloud | PORT 8883 (TLS)``` Encription ready.
	- Here are the details of our cluster
	![HiveMQ Cluster Details](/images/hivemq1.png)
	- Credentials to publish and subscribe are:
	```galeoiot-dev & 3J2Dj3p7kHDz```
	- Check the broker is running and you are able to connect by using MQTT-Explorer or any other MQTT client.
	- Please note that free cluster doesn't have any monitoring console.


3. Get your favourite MQTT client (client or OS native) and configure your broker
	- In this example, we are going to use [MQTT Explorer](http://mqtt-explorer.com/) _Thanks to Thomas Nordquist thomasnordquist_
	- Configure the broker settings:
		- Broker Name
		- Broker url or in our case IP
		- Broker port (default 1883)
		- Broker user & passwd

![Image of MQTT config](/images/mqttexplorerconfig.png)

4. Access the broker and quick-ckeck the data

![Image of MQTT Data](/images/mqttexplorerdata.png)

5. Activate the smart lamp to force a temperature rising (and the opossite effect in rel. humidity)
 Use the SmartLife App to activate the lamp and check the result in the real time charts at the MQTT client.

 ![Image Lamp](/images/Lamp.PNG)
