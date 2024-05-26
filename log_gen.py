import json
import random
from datetime import datetime
from time import sleep

import numpy as np
import requests


def simulate_log_data(application_id: int) -> str:
    """
    Simulate log data for a given application ID, generating logs with different
    levels, response types, and other attributes.

    Args:
        application_id: Integer representing the application ID.

    Returns:
        JSON string containing the simulated log data.
    """
    urls = ["/api/data", "/api/info", "/api/login", "/api/logout"]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    ]
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    messages = [
        "User logged in successfully",
        "User attempted a failed login",
        "Database connection failed",
        "Data fetched successfully",
        "Invalid user input",
    ]
    response_statuses = [200, 404, 500, 200, 400]  # Matched with messages
    weights = [0.6, 0.05, 0.15, 0.1, 0.1]  # Frequency of each message type

    message_index = np.random.choice(len(messages), p=weights)

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "application_id": f"app_{application_id}",
        "log_level": random.choice(log_levels),
        "error_code": response_statuses[message_index],
        "message": messages[message_index],
        "request_type": random.choice(["GET", "POST", "PUT", "DELETE"]),
        "url": random.choice(urls),
        "user_agent": random.choice(user_agents),
        "session_id": f"session_{random.randint(1, 10)}",
        "response_time_ms": (
            random.randint(100, 1000)
            if response_statuses[message_index] == 200
            else None
        ),
    }
    return json.dumps(log_data)


def send_log_to_server(log_data: str) -> None:
    """
    Send the log data to a web server.

    Args:
        log_data: JSON string containing the log data.

    Returns:
        None
    """
    url = "https://5000-snone-rtdatastream-kmzlmqy3zlk.ws-eu114.gitpod.io/logs"  # Replace with your server endpoint
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=log_data, headers=headers)
    if response.status_code == 200:
        print("Log sent successfully")
    else:
        print(f"Failed to send log: {response.status_code}, {response.text}")


def produce_data() -> None:
    """
    Continuously produce simulated log data for multiple applications.

    Sends the data to a web server.
    """
    application_count = 3  # Number of different applications
    while True:
        for application_id in range(1, application_count + 1):
            data = simulate_log_data(application_id)
            send_log_to_server(data)
            print(f"Sent data: {data}")
        sleep(0.1)  # Simulate log production delay


if __name__ == "__main__":
    produce_data()
