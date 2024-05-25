# Real-Time Application Metrics Dashboard

## Overview

This project demonstrates a real-time interactive dashboard for mimicking application metric data, leveraging powerful big data tools such as Apache Kafka and Apache Spark. It serves as an end-to-end template for building data engineering projects that utilize Apache Kafka, Apache Spark, and PostgreSQL database, all containerized with Docker.

## Features

- **Real-Time Data Processing**: Uses Apache Kafka for message queuing and Apache Spark for stream processing.
- **Interactive Dashboard**: Utilizes Plotly Dash to create dynamic and real-time visualizations of the processed data.
- **Modular Design**: The project is structured to be easily extensible for various use cases involving real-time data streams.
- **Ease of Setup**: Can be launched with a simple Docker Compose command.


## Architecture Overview

**1. Sensor Logger App (Flask Server)**
Purpose: Receives sensor data from various devices.
Technology Stack: Python (Flask), PostgreSQL (for storing sensor data).
Functionality: The core application that collects sensor readings and stores them in a database.
**2. Data Processing Pipeline**
Component 1: Kafka Producer
Purpose: Publishes sensor data from the Sensor Logger App to Kafka topics.
Technology Stack: Python (Kafka producer library).
Component 2: Kafka Consumer
Purpose: Consumes data from Kafka topics and processes it further.
Technology Stack: Apache Spark Streaming (or Structured Streaming for newer versions).
**3. Data Storage**
PostgreSQL Database
Purpose: Stores processed data for long-term storage and analysis.
Technology Stack: PostgreSQL.
**4. Data Visualization Dashboard**
Dash Application
Purpose: Provides interactive visualizations of stored data.
Technology Stack: Python (Dash framework).
**5. Data Analysis and Reporting**
Spark SQL / DataFrame API
Purpose: Performs complex data analysis and generates reports based on the stored data.
Technology Stack: Apache Spark.

## Workflow

**Data Collection:** The Sensor Logger App collects sensor data and sends it to the Kafka Producer.

**Data Processing:** The Kafka Consumer reads the incoming data and processes it using Spark Streaming or Structured Streaming.

**Data Storage:** Processed data is stored in the PostgreSQL database for long-term retention.

**Data Visualization:** The Dash application fetches data from the PostgreSQL database and displays it through interactive charts and graphs.
Analysis and Reporting: Additional processing and reporting can be performed using Spark SQL or DataFrame API on the stored data.

##Development Steps

Set up the Sensor Logger App: Develop the Flask server to collect sensor data and store it in PostgreSQL.
Implement Kafka Integration: Add Kafka producers and consumers to handle real-time data flow between the Sensor Logger App and the Spark processing engine.
Configure Spark Streaming: Set up Spark Streaming or Structured Streaming to process the incoming data streams.
Integrate PostgreSQL: Ensure the processed data is correctly stored in the PostgreSQL database.
Develop the Dash Dashboard: Create a Dash application to visualize the stored data interactively.
Add Analysis Capabilities: Utilize Spark SQL or DataFrame API for advanced data analysis and reporting.

### Prerequisites

Ensure you have Docker and Docker Compose installed on your machine. These tools are required to create the containerized environment for running the services.

### Installation

1. **Clone the Repository**

   Start by cloning this repository to your local machine using ssh:

   ```bash
   git clone git@github.com:firefly-cmd/data-engineering-template.git
   cd data-engineering-template

2. **Launch the services**

    Start the services with docker compose

   ```bash
    docker-compose up --build


3. **Checkout the dashboard**

    You can now go to the localhost:8050 to view the dashboard.

### Customization

    You can customize this template for your own projects by modifying the source code to adjust the data processing logic, the types of metrics displayed, or the visual appearance of the dashboard.