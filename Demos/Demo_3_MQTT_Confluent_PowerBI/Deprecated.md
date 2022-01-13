# Deprecated documentation but still useful.

## Demo Confluent-Repsol
Instrucciones para la implementación de la demo Confluent-Repsol.

### Componentes
|Directorio|Archivos|Descripción |
|-|------------------|----------------|
|**PartA**|ccloud_lib.py|Archivo de configuración, esquemas
||productor-11.py|Productor JSON 11 elementos
||productor-14.py|Productor JSON 14 elementos
|**PartB**|ccloud_lib.py|Archivo de configuración, esquemas|
||productor-3.py|Productor AVRO 3 elementos
||productor-4.py|Productor AVRO 4 elementos
|**PartC**|ccloud_lib.py|Archivo de configuración, esquemas|
||demo-conflunet-telemetry-mqtt.py|Pasarela MQTT-Confluent AVRO
|**demo_consumers**|consumer_alert.py|Gestión de alertas Confluent
||consumer_iot_telemetry.py|Consumidor Topic Confluent
|**.confluent**|librdkafka.config|Archivo de configuración Confluent
|[Drive](https://drive.google.com/file/d/1zmnsOT3FDLR6T859QC4PI89GuVS8FqXC/view?ts=5ea2a124)|Demo Confluent-Repsol.pptx|Presentación Demo
|ficheros de prueba|/ficheros_de_prueba|Pruebas varias y otros programas válidos descartados para la demo
|raspberry|sender_raspi.py|Lectura de sensores y envío MQTT de los resultados

### Variables configuración
1. Archivo de configuración Confluent: `/home/ubuntu/.confluent/librdkafka.config`
	>#Kafka
	bootstrap.servers=pkc-lz6r3.northeurope.azure.confluent.cloud:9092
	security.protocol=SASL_SSL
	sasl.mechanisms=PLAIN
	sasl.username=QOWBA2FFPE3RZY5Y
	sasl.password=7sWRXalpEPrVFIxi5LyYdF2dJq6P9Afx0uMiUSy3f1PQNANun8siDNopzNrzqAJs
	#Confluent Cloud Schema Registry
	schema.registry.url=https://psrc-4kk0p.westeurope.azure.confluent.cloud
	basic.auth.credentials.source=USER_INFO
	schema.registry.basic.auth.user.info=MS532AADUMAFZBY2:i0NRwZGfvgiG4WF8+/+xMRNf3Ts29jy68fEt7HvjrOcGOy9X/l8/6orlG0Da+zmz

2. Configuración acceso a Broker MQTT en el archivo: `demo-confluent-telemetry-mqtt.py`
	>USER_MQTT = "galeo"
	PASSWORD_MQTT = "Hq93*alrEYD98oPT"
	TOPIC_MQTT = 'galeo_mqtt'
	CLIENT_ID_MQTT = 'galeo-subs'
	HOST_MQTT = '127.0.0.1'
	PORT_MQTT = 1883

3. Los esquemas necesarios para cada ejemplo, se pueden ver dentro del *Guión Demo 	Confluent-Repsol*, en este repositorio.
4. Los datos MQTT necesarios para el envío desde la Raspberry, son los mismos que en el punto 2.

### Requisitos infraestructura, aplicaciones y librerías
1. Máquina Ubuntu. En este caso desplegada en una EC2 de AWS.
2. Librerías *librdkafka* y * Confluent-kafka*. Ver instrucciones [aquí](https://github.com/confluentinc/confluent-kafka-python).
3. Librería *schedule*. [Enlace](https://pypi.org/project/schedule/)
4. Broker MQTT Mosquitto. Ver instrucciones de instalación [aquí](https://www.nociones.de/instalacion-de-mosquitto-para-mqtt/).
5. Abrir puerto 1883 para comunicaciones externas con Mosquitto en AWS. Instrucciones [aquí](https://medium.com/@victormagallanes2/crear-instancia-en-aws-ec2-vps-abrir-puertos-5993a418a1a1)
6. Raspberry con Raspbian, cliente *Mosquitto* y lectura del sensor SHT71 vía I2C. Instrucciones [aquí](https://pypi.org/project/sht-sensor/). Cuenta activa en *Weatherstack* para obtener datos meteorológicos. [Enlace](https://weatherstack.com/).

### Ejecucción y despliegue software
Seguir la guía *Guión Demo Confluent-Repsol* en este mismo repositorio.

### Presentación
Ver presentación *Demo Confluent-Repsol.pptx* [aquí](https://drive.google.com/file/d/1zmnsOT3FDLR6T859QC4PI89GuVS8FqXC/view?ts=5ea2a124).


