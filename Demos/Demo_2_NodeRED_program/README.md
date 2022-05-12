# Demo 2. NodeRED program

# Demo 2 Intro

In this demo we are going to use NodeRED as a code-less automation framework. In the first demo we retrieved the sensors' readings from the MQTT topic. With a MQTT client we were able to visualize the data trends and data changes but not too much. A MQTT client is designed to inspect the data but no actuate or program actions. Of course, we have always the possibility to program our own MQTT client and then, adding more functionalities by code. But, to do this we need advanced programming skills. 

# Prerequisites

1. __An MQTT broker__ up and getting messages. Please, see the [demo1](/Demos/Demo_1_MQTT_and_IoT_Setup) to check-out the set-up. To have a quick idea if the MQTT broker is up&running execute look for data at the MQTTExplorer tool.

2. __A node-red installed__ in the VM. If so, just open ```http://ec2-54-173-46-11.compute-1.amazonaws.com:1880``` in your local browser. Please, have in mind that 1880 port must be enable for traffic at the VM security control menu in the AWS console.

3. __The node-red__ automation program for this demo. Create an empty new flow and import the sample program ```Node-red-sample-program.json``` located [here](Demos/Demo_2_NodeRED_program) at this repository. This node-red flow uses the following packages inside node-red. Please, have in mind if you start from a fresh node-red installation you must install the following packages at the palette menu before to _Deploy_ the program.

- node-red-contrib-telegrambot
- node-red-dashboard


Let's do this step-by-step

0. Check the set up.

 1. __Node-RED__ program. Import the node-red program and configure the MQTT node to the corresponding broker parameters. Observe the built-in NodeRED program and listen the explanation.

 ![Image Webcam](/images/nodered-programm.png)
 
 2. __Node-RED Dashboard__ .Open the dashboard and observe the behavior.

 ![Image Webcam](/images/nodered-dashboard.png)

 3. __Integrations. The Telegram Bot__ . One super-fun thing we can do with node-red and many other IoT platforms are the integrations. In this case, we're going to integrate our monitoring program with a Telegram Bot just to triggers temperature alerts. 

 To check our bot is properly configure just do the following:

 - Open Telegram App and call __Botfather__
 - Execute ```/mybots``` and select your bot
 - Click on ```API Token``` to retrieve the Bot Token.
 - Copy & Paste the Token into the Telegram node in the node-red programm

 Check the telegram-bot and see what happens when we rise an alarm.

 ![Image Webcam](/images/telegrambot.png)

 4. Observe the next functionalities like create a notification dashboard or change the sampling dynamically by publishing a the sampling in seconds (1,5,10,...) in the ```cmnd/sampling``` topic.

 ![Dashboard notification and sampling](/images/notifications_sampling.png)

 5. It's time to play. It's your time :)
