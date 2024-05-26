import json
import random
from datetime import datetime
from time import sleep

import numpy as np
from confluent_kafka import Producer


# Configure Kafka Producer
conf = {
    "bootstrap.servers": "kafka:9092",
    "client.id": "log-producer",
    "api.version.request": True,
    "security.protocol": "PLAINTEXT",
}

producer = Producer(conf)


def delivery_report(err, msg) -> None:
    """
    Callback for reporting the delivery status of a message.

    Args:
        err: Error information if the message failed to deliver.
        msg: Message object if the delivery was successful.

    Returns:
        None
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def simulate_sensor_data() -> dict:
    """
    Simulate sensor data for accelerometer, gyroscope, gravity, orientation, and magnetometer.

    Returns:
        Dictionary containing the simulated sensor data.
    """
    return {
        "accelerometer": {
            "x": random.uniform(-10, 10),
            "y": random.uniform(-10, 10),
            "z": random.uniform(-10, 10),
            "timestamp": datetime.now().isoformat()
        },
        "gyroscope": {
            "x": random.uniform(-500, 500),
            "y": random.uniform(-500, 500),
            "z": random.uniform(-500, 500),
            "timestamp": datetime.now().isoformat()
        },
        "gravity": {
            "x": random.uniform(-10, 10),
            "y": random.uniform(-10, 10),
            "z": random.uniform(-10, 10),
            "timestamp": datetime.now().isoformat()
        },
        "orientation": {
            "pitch": random.uniform(-180, 180),
            "roll": random.uniform(-90, 90),
            "yaw": random.uniform(0, 360),
            "qw": random.uniform(-1, 1),
            "qx": random.uniform(-1, 1),
            "qy": random.uniform(-1, 1),
            "qz": random.uniform(-1, 1),
            "timestamp": datetime.now().isoformat()
        },
        "magnetometer": {
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
            "z": random.uniform(-100, 100),
            "timestamp": datetime.now().isoformat()
        }
    }

def produce_data() -> None:
    """
    Continuously produce simulated sensor data.

    Sends the data to a Kafka topic with a callback for delivery reports.
    """
    while True:
        data = simulate_sensor_data()
        producer.poll(0)
        producer.produce("sensor-logs", value=json.dumps(data), callback=delivery_report)
        print(f"Sent data: {json.dumps(data)}")
        producer.flush()
        sleep(0.1)  # Simulate log production delay

if __name__ == "__main__":
    produce_data()
