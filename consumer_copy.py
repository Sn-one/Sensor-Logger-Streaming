from confluent_kafka import Consumer, KafkaException
import json

def print_messages(consumer):
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(json.loads(msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    conf = {'bootstrap.servers': 'kafka:9092',
            'group.id': 'my-group',
            'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    consumer.subscribe(['sensor_logs'])

    print_messages(consumer)
