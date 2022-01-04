from confluent_kafka import Consumer


c = Consumer({
    'bootstrap.servers': 'pkc-43n10.us-central1.gcp.confluent.cloud:9092',
    'group.id': '0',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['prueba3'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
