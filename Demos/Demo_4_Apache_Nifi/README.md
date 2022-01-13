## Intro

This demo is about using Apache nifi event-driven data orchestator to consume IoT data from an MQTT broker and visualize by using an Apache InfluxDB (time-series database) and grafana.

## Pre-requisites

- Get up and run the MQTT broker with the ```telemetry``` topic has been used in previous demos.
- Get the broker url, username, passwd and port.
- Install (MACOS only)[Apache nifi](https://nifi.apache.org/docs/nifi-docs/html/getting-started.html#for-linux-macos-users) and start the service
	```brew install nifi``` navigate where the nifi directori is and eexecute ```bin/nifi.sh start```
- Install InfluxDB
	```brew update & brew install influxdb@1```
- Run InfluxDB
	```/usr/local/opt/influxdb/bin/influxd version```
	```/usr/local/opt/influxdb/bin/influx -precision rfc3339```
- Create a Data Base
	```CREATE DATABASE mydb```
	```USE mydb```
- Once we have finished the configuration of the other components we will be ready to query our timeseries database
	```SELECT * FROM telemetry```

- Install and run GRAFANA
	```brew update & brew install grafana```
	```brew services start grafana```
- Access Grafana in ```localhost:3000```


## Configuring Apache Nifi

- Access ```localhost:8080/nifi```
- Look for ConsumeMQTT processor
- Install InfluxDB ad-hoc processor ( [follow this documentation first](https://github.com/influxdata/nifi-influxdb-bundle) )
- Look for PutInfluxDatabaseRecord
- See the [ScreenShoots](./ScreenShoots) to understand how to configure the processors.
- Select all nodes and START the nodes.

## Check the data at the InfluxDB

- Open a terminal
	- Run InfluxDB
	```/usr/local/opt/influxdb/bin/influxd version```
	```/usr/local/opt/influxdb/bin/influx -precision rfc3339```
	```USE mydb```
	```SELECT * FROM telemetry```

## Visualize data in Grafana

- Acces to grafana interface
	```localhost:3000```
- Go to data sources and configure a new InfluxDB data source
- Create the dashboard (look at the [ScreenShoots](./ScreenShoots))



## References

[Tutorial IoT](https://www.baeldung.com/iot-data-pipeline-mqtt-nifi)
[Influx Nifi processor JSON2In-line](https://github.com/influxdata/nifi-influxdb-bundle)
[Grafana](https://grafana.com/docs/grafana/latest/installation/)

