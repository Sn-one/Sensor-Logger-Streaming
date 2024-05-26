import json
from datetime import datetime
from flask import Flask, request, jsonify
from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

# Configure Kafka Producer and Admin Client
conf = {
    "bootstrap.servers": "kafka:9092",
    "client.id": "log-producer",
    "api.version.request": True,
    "security.protocol": "PLAINTEXT",
}

producer = Producer(conf)
admin_client = AdminClient(conf)

app = Flask(__name__)

def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    """
    Create a Kafka topic if it doesn't exist.

    Args:
        topic_name: Name of the topic to create.
        num_partitions: Number of partitions for the topic.
        replication_factor: Replication factor for the topic.

    Returns:
        None
    """
    topic_metadata = admin_client.list_topics(timeout=5)
    if topic_name in topic_metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
        return

    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    fs = admin_client.create_topics([new_topic])
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic '{topic}' created successfully.")
        except KafkaException as e:
            if e.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
                print(f"Failed to create topic '{topic}': {e}")
            else:
                print(f"Topic '{topic}' already exists (concurrent creation).")

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

def filter_and_structure_data(data):
    """
    Filter and structure the incoming log data.

    Args:
        data: The raw log data.

    Returns:
        dict: The structured log data.
    """
    # Extract the necessary fields
    structured_data = {
        "messageId": data.get("messageId"),
        "sessionId": data.get("sessionId"),
        "deviceId": data.get("deviceId"),
        "timestamp": datetime.now().isoformat(),
        "sensors": []
    }
    
    for sensor in data.get("payload", []):
        sensor_data = {
            "name": sensor.get("name"),
            "time": sensor.get("time"),
            "values": sensor.get("values"),
        }
        if "accuracy" in sensor:
            sensor_data["accuracy"] = sensor["accuracy"]
        
        structured_data["sensors"].append(sensor_data)
    
    return structured_data

@app.route('/logs', methods=['POST'])
def receive_log():
    """
    Receive log data from HTTP POST request, filter, and send it to Kafka.

    Returns:
        JSON response indicating success or failure.
    """
    log_data = request.get_json()
    if not log_data:
        return jsonify({"error": "Invalid log data"}), 400
    
    try:
        create_kafka_topic("logs")
        structured_data = filter_and_structure_data(log_data)
        log_data_str = json.dumps(structured_data)
        producer.produce("logs", value=log_data_str, callback=delivery_report)
        producer.poll(0)
        return jsonify({"status": "Log sent to Kafka"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
