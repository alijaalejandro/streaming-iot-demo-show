# Demo 3 Intro. MQTT and Kafka Confluent

In this demo we are able, based on previous demos, to:

- Generate real-time data (environmental data) from:
    - Public Meteo Data
    - Temperature & Humidity (and dew point) data from a digital sensor.

Data is gathered into a Raspberri Pi by using a Python program and then sent to an MQTT broker on AWS VM. [sender-raspi](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Assets/raspberry/)

In this AWS VM, a SW agent written in python too, is acting as a gateway between the MQTT and Kafka-Confluent Cloud platform.
This program implements a Confluent-kafka producer that sends data to the galeo-dev-iot-telemetry topic. [mqtt-sender](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Assets/PartC/demo-confluent-telemetry-mqtt.py)

The program is retransmiting the telemetry data coming from the raspberripy. Now a kafka consumer [consumer-to-pbi](https://bitbucket.org/galeoteam/streaming-iot-demo-show/src/master/Assets/demo_consumers/) written in python is consuming the data in the telemetry topic and publishing this data into the Power BI Rest API for Streaming datasets. This streaming dataset is named Kafka-Confluent-Demo and this is the endpoint ```https://api.powerbi.com/beta/fb16d55e-d466-49fc-b4dc-4d5ec301ec20/datasets/3d316f87-2f9c-4525-bb89-5e28ce4b628d/rows?noSignUpCheck=1&key=wSDr%2Bc7%2BYHmSyrBlTs7wBpkIKpQa%2BJ5meUX7zmDdzpyU%2FTuiD7huUGAm9IxfowCnB65MMMv8YmSTg%2BQZNHzBvA%3D%3D``` with the following schema:

```json
[
{
"temperature_inside" :98.6,
"humidity_inside" :98.6,
"dew_point_inside" :98.6,
"temperature" :98.6,
"humidity" :98.6,
"wind_speed" :98.6,
"uv_index" :98.6,
"weather_descriptions" :98.6,
"pressure" :98.6,
"precip" :98.6,
"visibility" :98.6,
"wind_degree" :98.6,
"feelslike" :98.6,
"cloudcover" :98.6,
"datetime" :"2021-04-27T11:23:54.012Z"
}
]
```

![Image of PowerBI Dashboard](/images/PowerBIDashboard.png)

## KSQL-DB

A capability we want to demonstrate in this demo is the ability to perform real-time calculations by using one-single data platform. In this case, we are using the KSQL functionality to create an alarm module. Once the telemetry data in coming from the ```galeo-dev-iot-telemetry```topic, we can create an stream in KSQL and hence calculate real-time queries over the data.

In this case, we want to look at one field "temperature_inside" from the telemetry topic. We wnat to check if this value is above the certain threshold. In this case, we rise an over-temperature alarm. Of course, we want to produce this alarms in a new topic, so the KSQL engine, produce alarm data into a new topic ```galeo-dev-iot-alarms```

In our case this is the kind of query we execute:

```SQL
CREATE STREAM "galeo-dev-iot-alerts-meteo" as
    SELECT "temperature_inside" as "TemperatureValue",
        (CASE WHEN "temperature_inside" >= 30 
        THEN '30'
        WHEN "temperature_inside" >= 25
        THEN '25' 
        ELSE '< 25' END) as "TemperatureThreshold",
        (CASE WHEN "temperature_inside" >= 30 
        THEN 'Critical'
        WHEN "temperature_inside" >= 25 
        THEN 'Warning' 
        ELSE 'OK' END) as "AlertType"
    FROM "ksql-alerts"
EMIT CHANGES;
```


Now, we can see the output with this query: ```select * from "galeo-dev-iot-alerts-meteo" emit changes;``` and ```select * from "ksql-alerts" emit changes;```


![Image of KSQLDB](/images/ksqldb.png)








