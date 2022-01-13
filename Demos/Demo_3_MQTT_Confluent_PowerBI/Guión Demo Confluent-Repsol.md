# Guión Demo Confluent-Repsol
#### Parámetros de acceso al servidor de AWS
Abrir una sesión SSH en Moba con los siguientes parámetros:
- IP: 18.224.3.98
- User: ubuntu
- User private key: `GaleoAmazon.pem` (archivo adjunto)
- Directorio de trabajo: `/home/ubuntu/demoConfluent`
- Lenguaje: Python 2.7
- Archivo de configuración Confluent:
	- `librdkafka.config` (archivo adjunto)
	- Ruta: `/home/ubuntu/.confluent/`

Abrir una sesión SSH en la terminal MAC:
`ssh -i "Galeo Amazon.pem" ubuntu@ec2-18-224-3-98.us-east-2.compute.amazonaws.com`


## PartA. Topics Creados
**Directiorio: `/home/ubuntu/demoConfluent/PartA/`**
Pasos a seguir para preparar y ejecutar la demo:
1. Crear el Topic **galeo-dev-iot-telemetry**.
2. Crear el primer esquema de 11 elementos (esquemas *Value* y *Key*):
> `{
"doc": "Telemetry schema for sensor data of end-nodes",
"fields": [
{
"name": "temperature",
"type": "int"
},
{
"name": "humidity",
"type": "int"
},
{
"name": "wind_speed",
"type": "int"
},
{
"name": "uv_index",
"type": "int"
},
{
"name": "weather_descriptions",
"type": "int"
},
{
"name": "pressure",
"type": "int"
},
{
"name": "precip",
"type": "int"
},
{
"name": "visibility",
"type": "int"
},
{
"name": "wind_degree",
"type": "int"
},
{
"name": "feelslike",
"type": "int"
},
{
"name": "cloudcover",
"type": "int"
}
],
"name": "value_galeo_dev_iot_telemetry",
"namespace": "com.galeo.galeo-dev-kafka",
"type": "record"
}`

>`{
  "fields": [
    {
      "name": "name",
      "type": "string"
    }
  ],
  "name": "key_galeo_dev_iot_telemetry",
  "namespace": "com.galeo.galeo-dev-kafka",
  "type": "record"
}`

3. Definir el modo de compatibilidad en *Forward* en ambos esquemas, explicando el por qué.

 **TENER EN CUENTA QUE AL ESTAR UTILIZANDO MENSAJES JSON, SI ENVIAMOS CUALQUIERA DE ELLOS, AUNQUE SEA CON OTRO ESQUEMA, ENTRARÁN SIN PROBLEMA**
 **NO SE PUEDE VER EL BLOQUE POR ESQUEMA EN ESTE CASO DEBIDO A LOS MENSAJES JSON Y A LA DEFINICIÓN DE COMPATIBILIDAD FORWARD**

 4. Envío desde Productor de 11 elementos. **Enviaremos JSON, no esquema, para solucionar la visualización**:
> `python /home/ubuntu/demoConfluent/PartA/productor-11.py -f /home/ubuntu/.confluent/librdkafka.config -t galeo-dev-iot-telemetry`
 5. Parar ejecucción del programa tras un par de subidas y enseñan los datos recibidos.
 6. Registramos esquema de 14 elementos (solamente *Value*, *Key* es común):
 > `{
"doc": "Telemetry schema for sensor data of end-nodes",
"fields": [
{
"name": "temperature_inside",
"type": "int"
},
{
"name": "humidity_inside",
"type": "int"
},
{
"name": "power_inside",
"type": "int"
},
{
"name": "temperature",
"type": "int"
},
{
"name": "humidity",
"type": "int"
},
{
"name": "wind_speed",
"type": "int"
},
{
"name": "uv_index",
"type": "int"
},
{
"name": "weather_descriptions",
"type": "int"
},
{
"name": "pressure",
"type": "int"
},
{
"name": "precip",
"type": "int"
},
{
"name": "visibility",
"type": "int"
},
{
"name": "wind_degree",
"type": "int"
},
{
"name": "feelslike",
"type": "int"
},
{
"name": "cloudcover",
"type": "int"
}
],
"name": "value_galeo_dev_iot_telemetry",
"namespace": "com.galeo.galeo-dev-kafka",
"type": "record"
}`

7. Envío desde Productor de 14 elementos. **Enviaremos JSON, no esquema, para solucionar la visualización**:
> `python /home/ubuntu/demoConfluent/PartA/productor-14.py -f /home/ubuntu/.confluent/librdkafka.config -t galeo-dev-iot-telemetry`

8. Enseñamos los datos del segundo envío.

## PartB. Eventos
Este ejemplo simulará un Topic crítico de alertas.

1. Creamos el Topic **galeo-dev-iot-events**.
2. Definimos el esquema para 3 elementos (*Value* y *Key*):
> `{
"fields": [
{
"name": "machineid",
"type": "string"
},
{
"name": "machine_status",
"type": "string"
},
{
"name": "machine_critical_stop",
"type": "string"
}
],
"name": "value_galeo_dev_iot_events",
"namespace": "galeo.tech",
"type": "record"
}`

>`{
  "fields": [
    {
      "name": "name",
      "type": "string"
    }
  ],
  "name": "key_galeo_dev_iot_events",
  "namespace": "galeo.tech",
  "type": "record"
}`

3. Definimos la compatibilidad de los esquemas a **Full**.
4. Enviamos desde Productor de 3 elementos en **avro**:
> `python /home/ubuntu/demoConfluent/PartB/productor-3.py -f /home/ubuntu/.confluent/librdkafka.config -t galeo-dev-iot-events`
5. Enseñamos los datos. (Recordar que aunque los datos sean un tipo *int*, su representación va a ser errónea al ser un mensaje *avro*).
6. Enviamos desde Productor de 4 elementos en **avro**, conteniendo esquema de 3 elementos:
> `python /home/ubuntu/demoConfluent/PartB/productor-4.py -f /home/ubuntu/.confluent/librdkafka.config -t galeo-dev-iot-events`

Este productor tiene el siguiente esquema *Value*:
>`{
"fields": [
{
"name": "machineid",
"type": "string"
},
{
"name": "machine_status",
"type": "string"
},
{
"name": "machine_critical_stop",
"type": "string"
},
{
"name": "machine_revision",
"type": "string"
}
],
"name": "value_galeo_dev_iot_events",
"namespace": "galeo.tech",
"type": "record"
}`

7. Mostramos el error:
> `confluent_kafka.avro.error.ClientError: Incompatible Avro schema:409`

## PartC. Consumidor y Panel
En este ejemplo la Raspberry enviará datos vía MQTT y un programa de enlace en AWS subscrito a ese topic mqtt los enlazará a Confluent. A continuación un consumidor los pasará a un panel de PowerBI.

1. Creamos el topic ´galeo-dev-iot-telemetry-meteo` con 14 elementos, con el siguente esquema:
`{
"namespace": "com.galeo.galeo-dev-kafka",
"name": "value_galeo_dev_iot_telemetry",
"type": "record",
"fields": [ {"name": "temperature_inside", "type": "float"}, {"name": "humidity_inside", "type": "float"}, {"name": "dew_point_inside", "type": "float"}, {"name": "temperature", "type": "int"}, {"name": "humidity", "type": "int"}, {"name": "wind_speed", "type": "int"}, {"name": "uv_index", "type": "int"}, {"name": "weather_descriptions", "type": "int"}, {"name": "pressure", "type": "int"}, {"name": "precip", "type": "int"}, {"name": "visibility", "type": "int"}, {"name": "wind_degree", "type": "int"}, {"name": "feelslike", "type": "int"}, {"name": "cloudcover", "type": "int"} ]
}`

`{"namespace": "com.galeo.galeo-dev-kafka", "name": "key_galeo_dev_iot_telemetry", "type": "record", "fields": [ {"name": "name", "type": "string"}]}`

2. Levantamos el programa puente: `python /home/ubuntu/deemoConfluent/PartC/demo-confluent-telemetry-mqtt.py -f /home/ubuntu/.confluent/librdkafka.config -t galeo-dev-iot-telemetry-meteo`
3. Lanzamos datos de 14 elementos desde la Raspberry: `python3 sender_raspi.py 2 galeo_mqtt`
4. En este momento deberíamos poder verlos en el panel, y con ello el consumidor.

##### Notas PartC:
- La alarma KSQL se fijará en el parámetro 'temperature_inside' a un valor igual o superior a 25.
- Los datos del broker MQTT son los siguientes:
USER_MQTT = "galeo"  
PASSWORD_MQTT = "Hq93*alrEYD98oPT"  
TOPIC_MQTT = 'galeo_mqtt'  
CLIENT_ID_MQTT = 'galeo-subs'  
HOST_MQTT = '127.0.0.1'  (máquina AWS en 18.224.3.98)
PORT_MQTT = 1883
