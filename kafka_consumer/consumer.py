from confluent_kafka import Consumer, KafkaError
import psycopg2
from json import loads

def main():
    # Kafka consumer configuration
    conf = {'bootstrap.servers': 'kafka:9092',
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest'}

    # Create Kafka consumer
    c = Consumer(conf)
    c.subscribe(['sensor_logs'])

    # PostgreSQL connection parameters
    db_params = {
        "dbname": "sensor_logs",
        "user": "admin",
        "password": "admin",
        "host": "rt-data-stream-postgres-1",
        "port": "5432"
    }

    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Create messages table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            value TEXT NOT NULL
        );
    """)
    conn.commit()

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Insert message into PostgreSQL
            message_value = msg.value().decode('utf-8')  # Assuming message is a string
            cursor.execute("INSERT INTO messages (value) VALUES (%s)", (message_value,))
            conn.commit()

            # Print the consumed message
            print(f'Received message: {message_value}')

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        c.close()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
