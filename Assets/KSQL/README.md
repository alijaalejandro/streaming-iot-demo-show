
# KSQL

Setting up KSQLdb-server and KSQLdb-cli

## Setup

### SSH
```shell
chmod 400 "GaleoIoTKeys.pem"
ssh -i "GaleoIoTKeys.pem" ubuntu@ec2-3-138-103-174.us-east-2.compute.amazonaws.com
```


### KSQLdb-server

Deploy KSQLdb-server with Docker  
Set variables API_KEY_SCHEMA_REGISTRY, API_SECRET_SCHEMA_REGISTRY, API_KEY_CCLOUD and API_SECRET_CCLOUD
```shell
sudo docker run -d -p 8088:8088 \
-e KSQL_BOOTSTRAP_SERVERS=pkc-lz6r3.northeurope.azure.confluent.cloud:9092 \
-e KSQL_LISTENERS=http://0.0.0.0:8088 \
-e KSQL_KSQL_SERVICE_ID=ksqldbtest_ \
-e KSQL_KSQL_SINK_REPLICAS=3 \
-e KSQL_KSQL_STREAMS_REPLICATION_FACTOR=3 \
-e KSQL_KSQL_INTERNAL_TOPIC_REPLICAS=3 \
-e KSQL_KSQL_SCHEMA_REGISTRY_URL="https://psrc-4kk0p.westeurope.azure.confluent.cloud" \
-e KSQL_KSQL_SCHEMA_REGISTRY_BASIC_AUTH_CREDENTIALS_SOURCE="USER_INFO" \
-e KSQL_KSQL_SCHEMA_REGISTRY_BASIC_AUTH_USER_INFO="{API_KEY_SCHEMA_REGISTRY}:{API_SECRET_SCHEMA_REGISTRY}" \
-e KSQL_SECURITY_PROTOCOL=SASL_SSL \
-e KSQL_SASL_MECHANISM=PLAIN \
-e KSQL_SASL_JAAS_CONFIG="org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{API_KEY_CCLOUD}\" password=\"{API_SECRET_CCLOUD}\";" \
confluentinc/ksqldb-server
```


### KSQLdb-cli
Connect KSQLdb-cli with KSQLdb-server

```shell
sudo docker run --net=host --interactive --tty confluentinc/ksqldb-cli ksql http://localhost:8088
```


### Create Streams

Create KSQL stream from **galeo-dev-iot-telemetry** topic

```shell
CREATE STREAM "ksql-alerts" 
    ("uv_index" INT, 
    "weather_descriptions" INT, 
    "visibility" INT,
    "pressure" INT,
    "wind_speed" INT,
    "humidity_inside" INT,
    "temperature" INT,
    "cloudcover" INT,
    "humidity" INT,"precip" INT,
    "wind_degree" INT,
    "temperature_inside" INT,
    "feelslike" INT,
    "power_inside" VARCHAR) 
with (KAFKA_TOPIC='galeo-dev-iot-telemetry', VALUE_FORMAT='JSON');
```

Create KSQL stream for alerts
```shell
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