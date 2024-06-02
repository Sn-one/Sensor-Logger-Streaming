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
docker-compose up
