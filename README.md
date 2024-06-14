# Sensor-Logger-Streaming Project

## Overview

The Sensor-Logger-Streaming project is designed to process and visualize real-time sensor data using Kafka, Spark, PostgreSQL, and a Dash web application. This README answers key questions to ensure the system is reliable, scalable, maintainable, and secure.

## Architecture Diagram

![Architecture](https://github.com/Sn-one/Sensor-Logger-Streaming/blob/sensor-app_connected/sensor-logger-streaming_architecture.png)

## Key Components

### 1. Data Ingestion Microservices

- **Server**: Implemented using Flask, it receives sensor data from Kelvin Choi's Sensor Logger application and forwards it to Kafka.

### 2. Data Pre-processing and Aggregation Microservices

- **Spark Job**: Processes streaming data from Kafka, parsing JSON, applying schemas, and aggregating sensor metrics. The processed data is written to PostgreSQL.

### 3. Data Delivery to Frontend

- **Dash Application**: Provides real-time visualization of sensor data, fetching data from PostgreSQL and updating plots for different sensor metrics.

### 4. Reliability, Scalability, and Maintainability

- **Techniques**: 
  - Use of Kafka for scalable data ingestion and buffering.
  - Spark for scalable and fault-tolerant data processing.
  - Docker Compose for container orchestration ensuring reproducibility and easy deployment.
  - Version control with GitHub for code management.
  - Infrastructure as Code (IaC) principles.

### 5. Data Security, Governance, and Protection

- **Techniques**:
  - Secure Kafka communication using PLAINTEXT protocol (consider upgrading to SSL for production).
  - Secure PostgreSQL access with user authentication.
  - Isolation of services using Docker networks.

### 6. Docker Images

- **Images Used**:
  - `confluentinc/cp-zookeeper`
  - `confluentinc/cp-kafka`
  - `apache/spark:python3`
  - `postgres`
  - Custom images for Spark jobs, and Dash app


### 7. Data Source

- **Data Source**: Kelvin Choi's Sensor Logger application, simulating real-time sensor data.
- **Real-time Features**: Kafka for data streaming, Spark for processing.

### 8. Aggregation and Windowing Functions

- **Functions Used**:
  - Spark's `window` and `avg` functions to aggregate data over time windows for sensor metrics.

## Docker Compose Configuration

The `docker-compose.yml` file sets up the necessary services and their interdependencies, ensuring that all components can communicate and function together seamlessly.

### Services

- **Zookeeper**: Manages Kafka brokers.
- **Kafka**: Message broker for handling real-time data streams.
- **Spark Master & Worker**: Process the streaming data.
- **Postgres**: Stores processed sensor data.
- **Dash App**: Visualizes sensor data.

## Getting Started

To run the project, use the following command:

```bash
docker-compose --env-file .env_config up --build
```
### How to Connect the Sensor Logger Application to the Server in Docker

#### Steps to Connect the Sensor Logger Application

1. **Start the Server Container**:
   - Ensure the server container is running. Verify it by using:
     ```bash
     docker ps
     ```
   - Confirm that the container is exposed on port 5000.

2. **Identify the Docker Network**:
   - Find the network your server container is connected to, typically the default `bridge` network. List all Docker networks:
     ```bash
     docker network ls
     ```

3. **Inspect the Docker Network**:
   - Inspect the specific network to find details about connected containers and their IP addresses:
     ```bash
     docker network inspect bridge
     ```

4. **Locate Your Container's IP Address**:
   - In the network inspection output, locate your container by its name or ID. Find the `IPAddress` under the `Containers` section. For example:
     ```json
     "Containers": {
         "container_id": {
             "Name": "your_server_container",
             "IPAddress": "172.17.0.2",
             ...
         }
     }
     ```

5. **Configure Sensor Logger Application**:
   - Open the Sensor Logger application on your phone.
   - Navigate to the settings or configuration section where you can specify the server endpoint.
   - Set the endpoint URL to `http://<container_ip>:5000/sensor_data`.
     - Replace `<container_ip>` with the IP address found in the previous step, e.g., `172.17.0.2`.
   - Select the sensors to log in the Sensor Logger application. Ensure you select the following sensors as they are used in the project:
     - Accelerometer
     - Gyroscope
     - Gravity
     - Orientation
     - Magnetometer

6. **Send Data from Sensor Logger**:
   - Start sending data from the Sensor Logger application. The data should be posted to the specified endpoint on your server.
   - Verify that the server container is receiving the data by checking the server logs or database.

### Example Configuration for Sensor Logger

**Server URL**: `http://172.17.0.2:5000/sensor_data`  
**HTTP Method**: `POST`  
**Content-Type**: `application/json`

### Example cURL Command for Testing

You can use the following cURL command to send a sample JSON payload to your server endpoint for testing:

```bash
curl -X POST http://172.17.0.2:5000/sensor_data -H "Content-Type: application/json" -d '{
  "messageId": "msg123",
  "sessionId": "session456",
  "deviceId": "device789",
  "timestamp": "2023-01-01T00:00:00Z",
  "sensors": [
    {
      "name": "accelerometer",
      "time": 123456789,
      "values": {
        "x": 1.0,
        "y": 0.0,
        "z": -1.0
      },
      "accuracy": 0.98
    }
  ]
}'
```
Network Considerations
Ensure your host machine and phone running the Sensor Logger application are on the same local network for the connection to work.
If your Docker container is using a custom network, ensure that the network configurations allow communication between the container and your host machine.
By following these steps, you will be able to connect the Sensor Logger application to the server running in a Docker container and send data successfully.

### How to Connect the Sensor Logger Application to the Server in Docker Using Gitpod

#### Steps to Connect the Sensor Logger Application in Gitpod

1. **Start the Server Container**:
   - Ensure the server container is running. Verify it by using:
     ```bash
     docker ps
     ```
   - Confirm that the container is exposed on port 5000.

2. **Expose the Port in Gitpod**:
   - When running your server container in Gitpod, the port will be exposed to a public URL provided by Gitpod.
   - Find the URL by looking for the exposed port in Gitpod. It will look something like `https://5000-<your-gitpod-id>.ws-eu.gitpod.io`.

3. **Configure Sensor Logger Application**:
   - Open the Sensor Logger application on your phone.
   - Navigate to the settings or configuration section where you can specify the server endpoint.
   - Set the endpoint URL to the exposed URL from Gitpod, followed by the endpoint path. For example: `https://5000-<your-gitpod-id>.ws-eu.gitpod.io/sensor_data`.

4. **Send Data from Sensor Logger**:
   - Start sending data from the Sensor Logger application. The data should be posted to the specified endpoint on your server.
   - Verify that the server container is receiving the data by checking the server logs or database.

### Example Configuration for Sensor Logger

**Server URL**: `https://5000-<your-gitpod-id>.ws-eu.gitpod.io/sensor_data`  
**HTTP Method**: `POST`  
**Content-Type**: `application/json`

### Accessing the Dash Application in Docker or Gitpod

After starting all containers using Docker Compose, follow these steps to access the Dash application for viewing real-time sensor data.

#### Steps to Access the Dash Application

1. **Start All Containers**:
   - Run the following command to start all the containers as defined in your `docker-compose.yml` file:
     ```bash
     docker-compose up --build
     ```

2. **Check if the Containers are Running**:
   - Verify that all necessary containers are running, including the server, Kafka, Spark, PostgreSQL, and the Dash application:
     ```bash
     docker ps
     ```

3. **Access the Dash Application in Docker**:
   - If you are running Docker locally, the Dash application will be accessible at:
     ```
     http://localhost:8050
     ```

4. **Access the Dash Application in Gitpod**:
   - If you are using Gitpod, the port for the Dash application will be exposed to a public URL provided by Gitpod.
   - Find the URL by looking for the exposed port in Gitpod. It will look something like `https://8050-<your-gitpod-id>.ws-eu.gitpod.io`.

### Example URL Configuration for Local Docker

**Local Docker URL**: `http://localhost:8050`

### Example URL Configuration for Gitpod

**Gitpod URL**: `https://8050-<your-gitpod-id>.ws-eu.gitpod.io`

### Troubleshooting

- If you cannot access the application, ensure that the Docker containers are running without errors by checking the logs:
  ```bash
  docker-compose logs

