import json
from datetime import datetime
from flask import Flask, request, jsonify
from confluent_kafka import Producer

# Configure Kafka Producer
conf = {
    "bootstrap.servers": "kafka:9092",
    "client.id": "log-producer",
    "api.version.request": True,
    "security.protocol": "PLAINTEXT",
}

producer = Producer(conf)

app = Flask(__name__)

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

@app.route('/logs', methods=['POST'])
def receive_log():
    """
    Receive log data from HTTP POST request and send it to Kafka.

    Returns:
        JSON response indicating success or failure.
    """
    log_data = request.get_json()
    if not log_data:
        return jsonify({"error": "Invalid log data"}), 400
    
    try:
        log_data_str = json.dumps(log_data)
        producer.produce("logs", value=log_data_str, callback=delivery_report)
        producer.poll(0)
        return jsonify({"status": "Log sent to Kafka"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
