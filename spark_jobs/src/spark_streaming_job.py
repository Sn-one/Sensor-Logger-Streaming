from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    avg,
    to_timestamp,
    window,
    explode
)
from pyspark.sql.types import StructType, StructField, StringType, FloatType, LongType, ArrayType, MapType

def write_to_postgres(df, epoch_id, table_name: str) -> None:
    """
    Writes a DataFrame to PostgreSQL using JDBC.

    Args:
        df: DataFrame to write.
        epoch_id: Epoch ID of the streaming batch.
        table_name: Name of the PostgreSQL table.

    This function uses JDBC to append data to a PostgreSQL table, ensuring that
    data is persisted in a relational database for later analysis and reporting.
    """
    jdbc_url = "jdbc:postgresql://postgres:5432/logs"
    properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver",
    }
    df.write.jdbc(url=jdbc_url, table=table_name, mode="append", properties=properties)

def main() -> None:
    """
    Main function to initialize Spark session and process streaming data.
    """
    # Initialize Spark session for processing
    spark = SparkSession.builder.appName("KafkaSensorStream").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Kafka configuration details
    kafka_topic_name = "logs"
    kafka_bootstrap_servers = "kafka:9092"

    # Define the schema for the incoming sensor data
    schema = StructType([
        StructField("messageId", StringType(), True),
        StructField("sessionId", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("sensors", ArrayType(StructType([
            StructField("name", StringType(), True),
            StructField("time", LongType(), True),
            StructField("values", MapType(StringType(), FloatType()), True),
            StructField("accuracy", FloatType(), True)
        ])), True)
    ])

    # Read data from Kafka using structured streaming
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
        .option("subscribe", kafka_topic_name)
        .option("startingOffsets", "earliest")
        .load()
    )

    # Parse the JSON data and apply the schema
    json_df = df.selectExpr("CAST(value AS STRING) as json").select(
        from_json(col("json"), schema).alias("data")
    )

    # Explode the sensors array to get individual sensor data points
    exploded_df = json_df.select(
        col("data.messageId").alias("messageId"),
        col("data.sessionId").alias("sessionId"),
        col("data.deviceId").alias("deviceId"),
        col("data.timestamp").alias("recording_timestamp"),
        explode(col("data.sensors")).alias("sensor")
    ).select(
        col("messageId"),
        col("sessionId"),
        col("deviceId"),
        col("recording_timestamp"),
        col("sensor.name").alias("sensor_name"),
        col("sensor.time").alias("sensor_time"),
        col("sensor.values").alias("sensor_values"),
        col("sensor.accuracy").alias("sensor_accuracy")
    )

    # Flatten the sensor values
    flattened_df = exploded_df.select(
        "messageId",
        "sessionId",
        "deviceId",
        "recording_timestamp",
        "sensor_name",
        "sensor_time",
        col("sensor_values.x").alias("x_value"),
        col("sensor_values.y").alias("y_value"),
        col("sensor_values.z").alias("z_value"),
        col("sensor_values.yaw").alias("yaw"),
        col("sensor_values.pitch").alias("pitch"),
        col("sensor_values.roll").alias("roll"),
        col("sensor_values.qw").alias("qw"),
        col("sensor_values.qx").alias("qx"),
        col("sensor_values.qy").alias("qy"),
        col("sensor_values.qz").alias("qz"),
        "sensor_accuracy"
    )

    # Convert sensor_time to timestamp
    processed_df = flattened_df.withColumn(
        "sensor_timestamp", to_timestamp((col("sensor_time") / 1000000000).cast("timestamp"))
    )

    # Aggregate data based on sensor type and a sliding window
    sensor_metrics_df = processed_df.groupBy(
        window("sensor_timestamp", "10 seconds"), "sensor_name"
    ).agg(
        avg("x_value").alias("avg_x_value"),
        avg("y_value").alias("avg_y_value"),
        avg("z_value").alias("avg_z_value"),
        avg("yaw").alias("avg_yaw"),
        avg("pitch").alias("avg_pitch"),
        avg("roll").alias("avg_roll"),
        avg("qw").alias("avg_qw"),
        avg("qx").alias("avg_qx"),
        avg("qy").alias("avg_qy"),
        avg("qz").alias("avg_qz"),
    ).select(
        col("window.start").alias("startdate"),
        col("window.end").alias("enddate"),
        "sensor_name",
        "avg_x_value",
        "avg_y_value",
        "avg_z_value",
        "avg_yaw",
        "avg_pitch",
        "avg_roll",
        "avg_qw",
        "avg_qx",
        "avg_qy",
        "avg_qz"
    )

    # Setup the streaming query to write the aggregated results to PostgreSQL
    sensor_query = (
        sensor_metrics_df.writeStream.outputMode("update")
        .foreachBatch(
            lambda df, epoch_id: write_to_postgres(df, epoch_id, "sensor_metrics")
        )
        .start()
    )

    # Wait for all processing to be done
    sensor_query.awaitTermination()


if __name__ == "__main__":
    main()
