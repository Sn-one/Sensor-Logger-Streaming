from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    avg,
    to_timestamp,
    window,
)
from pyspark.sql.types import StructType, StructField, StringType, FloatType

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
    kafka_topic_name = "sensor-logs"
    kafka_bootstrap_servers = "kafka:9092"

    # Define the schema for the incoming sensor data
    schema = StructType([
        StructField("accelerometer", StructType([
            StructField("x", FloatType(), True),
            StructField("y", FloatType(), True),
            StructField("z", FloatType(), True),
            StructField("timestamp", StringType(), True),
        ]), True),
        StructField("gyroscope", StructType([
            StructField("x", FloatType(), True),
            StructField("y", FloatType(), True),
            StructField("z", FloatType(), True),
            StructField("timestamp", StringType(), True),
        ]), True),
        StructField("gravity", StructType([
            StructField("x", FloatType(), True),
            StructField("y", FloatType(), True),
            StructField("z", FloatType(), True),
            StructField("timestamp", StringType(), True),
        ]), True),
        StructField("orientation", StructType([
            StructField("pitch", FloatType(), True),
            StructField("roll", FloatType(), True),
            StructField("yaw", FloatType(), True),
            StructField("qw", FloatType(), True),
            StructField("qx", FloatType(), True),
            StructField("qy", FloatType(), True),
            StructField("qz", FloatType(), True),
            StructField("timestamp", StringType(), True),
        ]), True),
        StructField("magnetometer", StructType([
            StructField("x", FloatType(), True),
            StructField("y", FloatType(), True),
            StructField("z", FloatType(), True),
            StructField("timestamp", StringType(), True),
        ]), True),
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


    # Explode the JSON data into individual sensor data points
    sensor_df = json_df.select(
        col("data.accelerometer.x").alias("accel_x"),
        col("data.accelerometer.y").alias("accel_y"),
        col("data.accelerometer.z").alias("accel_z"),
        to_timestamp(col("data.accelerometer.timestamp")).alias("accel_timestamp"),

        col("data.gyroscope.x").alias("gyro_x"),
        col("data.gyroscope.y").alias("gyro_y"),
        col("data.gyroscope.z").alias("gyro_z"),
        to_timestamp(col("data.gyroscope.timestamp")).alias("gyro_timestamp"),

        col("data.gravity.x").alias("gravity_x"),
        col("data.gravity.y").alias("gravity_y"),
        col("data.gravity.z").alias("gravity_z"),
        to_timestamp(col("data.gravity.timestamp")).alias("gravity_timestamp"),

        col("data.orientation.pitch").alias("orientation_pitch"),
        col("data.orientation.roll").alias("orientation_roll"),
        col("data.orientation.yaw").alias("orientation_yaw"),
        col("data.orientation.qw").alias("orientation_qw"),
        col("data.orientation.qx").alias("orientation_qx"),
        col("data.orientation.qy").alias("orientation_qy"),
        col("data.orientation.qz").alias("orientation_qz"),
        to_timestamp(col("data.orientation.timestamp")).alias("orientation_timestamp"),

        col("data.magnetometer.x").alias("magnetometer_x"),
        col("data.magnetometer.y").alias("magnetometer_y"),
        col("data.magnetometer.z").alias("magnetometer_z"),
        to_timestamp(col("data.magnetometer.timestamp")).alias("magnetometer_timestamp"),
    )

    # Aggregate data based on sensor type and a sliding window
    sensor_metrics_df = sensor_df.groupBy(window("accel_timestamp", "10 seconds")).agg(
        avg("accel_x").alias("avg_accel_x"),
        avg("accel_y").alias("avg_accel_y"),
        avg("accel_z").alias("avg_accel_z"),
        avg("gyro_x").alias("avg_gyro_x"),
        avg("gyro_y").alias("avg_gyro_y"),
        avg("gyro_z").alias("avg_gyro_z"),
        avg("gravity_x").alias("avg_gravity_x"),
        avg("gravity_y").alias("avg_gravity_y"),
        avg("gravity_z").alias("avg_gravity_z"),
        avg("orientation_pitch").alias("avg_orientation_pitch"),
        avg("orientation_roll").alias("avg_orientation_roll"),
        avg("orientation_yaw").alias("avg_orientation_yaw"),
        avg("orientation_qw").alias("avg_orientation_qw"),
        avg("orientation_qx").alias("avg_orientation_qx"),
        avg("orientation_qy").alias("avg_orientation_qy"),
        avg("orientation_qz").alias("avg_orientation_qz"),
        avg("magnetometer_x").alias("avg_magnetometer_x"),
        avg("magnetometer_y").alias("avg_magnetometer_y"),
        avg("magnetometer_z").alias("avg_magnetometer_z"),
    ).select(
        col("window.start").alias("startdate"),
        col("window.end").alias("enddate"),
        "avg_accel_x",
        "avg_accel_y",
        "avg_accel_z",
        "avg_gyro_x",
        "avg_gyro_y",
        "avg_gyro_z",
        "avg_gravity_x",
        "avg_gravity_y",
        "avg_gravity_z",
        "avg_orientation_pitch",
        "avg_orientation_roll",
        "avg_orientation_yaw",
        "avg_orientation_qw",
        "avg_orientation_qx",
        "avg_orientation_qy",
        "avg_orientation_qz",
        "avg_magnetometer_x",
        "avg_magnetometer_y",
        "avg_magnetometer_z",
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
