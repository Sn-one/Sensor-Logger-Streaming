from confluent_kafka import Consumer, KafkaException

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'sensor-data-producer',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['sensor_logs'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        raise KafkaException(msg.error())
    else:
        print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()

