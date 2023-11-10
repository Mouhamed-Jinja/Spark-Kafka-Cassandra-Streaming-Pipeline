# Data Engineering Project

This project presents a comprehensive data streaming pipeline, integrating Python, Kafka, Spark Streaming, Docker, and Airflow. It enables streaming data from an API to Kafka, and subsequently to Cassandra using Spark Streaming. This project is designed to process, transmit, and analyze real-time data efficiently and at scale.

<img width="906" alt="streaming2" src="https://github.com/Mouhamed-Jinja/Spark-Kafka-Cassandra-Streaming-Pipeline/assets/132110499/d1780284-4124-4c6a-90f3-d73f94b4e491">

## Introduction
This repository leverages [Docker Compose](https://docs.docker.com/compose/) to set up the cluster infrastructure, which includes:

- Spark
- Kafka
- Cassandra
- Airflow
- Python

## Quick Start

1. Clone the repository and start the demo:
    ```
    https://github.com/Mouhamed-Jinja/Spark-Kafka-Cassandra-Streaming-Pipeline.git
    ```

2. Build the Airflow image, which is extended to run Spark jobs. The official Airflow-Spark image from the documentation is used. For more information, refer to the provided repository
- link:
  ```
  https://github.com/Mouhamed-Jinja/Airflow-spark-Postgres-integration.git
  ```
- Build command
  ```
  docker build -t airspark:4.0 .
  ```
3. Launch the Docker Compose file:
  ```
  docker-compose up -d
  ```

4. Install the Cassandra driver inside Spark nodes using pip. Alternatively, you can extend the Spark Bitnami image to include the Cassandra driver.
  ```
  pip intsll cassandra-driver
  ```

5. Install the Kafka API on your machine to enable the use of KafkaProducer and Consumer.
  ```
  pip install kafka-python
  ```
6. Finally, create the Kafka topic:
  ```
  docker exec -it broker
  kafka-topics --create --topic users --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
  ```

## Running the Application
After completing the setup steps, you are ready to start streaming.

1. Open the Airflow webserver UI and run the DAG.
  ```
  http://localhost:8080/login/
  ```
  -user: airflow
  -password: airflow

2. Alternatively, you can use the command line to run the application.
  - Run the Producer:
  ```
  cd app
  python kafka_streaming_producer.py
  ```
  - use spark-submit to run the spark Job
  ```
  docker exec -it spark-master bash
  cd app
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.0 spark.py
  ```

## Using "cqlsh" Cassandra Query Language Shell
You can use cqlsh to execute your SQL batch scripts on the data loaded into Cassandra.

- Enter the Cassandra container:
   ```
   docker exec -it cassandra bash
   ```
 - then use cassandra query lang shell
   ```
   cqlsh
   ```
 - start writing your queries, for example show the data
   ```
    SELECT * FROM created_users ; 
   ```
