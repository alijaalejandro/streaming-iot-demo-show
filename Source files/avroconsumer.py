from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError


c = AvroConsumer({
    'bootstrap.servers': 'pkc-43n10.us-central1.gcp.confluent.cloud:9092',
    'group.id': 'schema-registry',
    'schema.registry.url': 'https://psrc-4nrnd.us-central1.gcp.confluent.cloud'})

c.subscribe(['prueba3'])

while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value())

c.close()
