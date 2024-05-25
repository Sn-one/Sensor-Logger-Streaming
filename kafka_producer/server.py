import json
import random
from datetime import datetime
from flask import Flask, request
from confluent_kafka import Producer
import numpy as np

# Configure Kafka Producer
conf = {
    "bootstrap.servers": "kafka:9092",
    "client.id": "sensor-data-producer",
    "api.version.request": True,
    "security.protocol": "PLAINTEXT",
}

producer = Producer(conf)

app = Flask(__name__)

@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    """
    Endpoint to receive sensor data from the Sensor Logger application.
    Parses the incoming JSON payload and forwards it to a Kafka topic.
    """
    try:
        data = request.get_json()
        # Optionally, validate or preprocess the data here
        producer.produce("sensor_logs", value=json.dumps(data))
        producer.flush()  # Ensures the message is sent immediately
        return {"status": "success"}, 200
    except Exception as e:
        # Log the error instead of printing it directly
        app.logger.error(f"Error receiving sensor data: {e}")
        return {"status": "error", "message": str(e)}, 500

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
        app.logger.error(f"Message delivery failed: {err}")
    else:
        app.logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
