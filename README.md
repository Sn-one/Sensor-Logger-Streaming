# Sensor-Logger-Streaming Project

## Overview

The Sensor-Logger-Streaming project is designed to process and visualize real-time sensor data using a combination of Kafka, Spark, PostgreSQL, and a Dash web application. The project includes multiple components, each serving a specific role in the data processing pipeline.
![Architecture](https://github.com/Sn-one/Sensor-Logger-Streaming/blob/sensor-app_connected/sensor-logger-streaming_architecture.png)
## Components

### 1. Server

The server component, implemented using Flask, receives sensor data from Kelvin Choi's Sensor Logger application. This data is then forwarded to a Kafka topic for further processing.

### 2. Spark Job

A Spark job processes the streaming data from Kafka, parsing JSON, applying schemas, and aggregating sensor metrics. The processed data is then written to a PostgreSQL database.

### 3. PostgreSQL

A PostgreSQL database is used to store the aggregated sensor metrics for later analysis and visualization.

### 4. Dash Application

The Dash web application provides real-time visualization of sensor data. It includes multiple plots for different sensor metrics such as accelerometer, gyroscope, gravity, orientation, and magnetometer. Data is fetched from the PostgreSQL database and updated at regular intervals.

### 5. Docker Compose

The project is containerized using Docker Compose, which defines services for Zookeeper, Kafka, Kafka producer, Spark master, Spark worker, PostgreSQL, and Dash app, along with their configurations and dependencies.

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

