# Data Engineering Project

an end-to-end data streaming pipeline, seamlessly integrating Python, Kafka, Spark Streaming, Docker, and Airflow.for streaming data from API to kafka, and then streaming data to Cassandra using Spark streaming. Effortlessly process, transmit, and analyze real-time data with this comprehensive project, designed for efficient and scalable streaming applications


## Introduction
This repository uses [Docker Compose](https://docs.docker.com/compose/) to initialize the cluster inferstructure including the following:

- Spark
- Kafka
- Cassandra
- Airflow
- Python


## Quick Start

1- Just clone the repo
```
./start_demo.sh
```
2-Build airflow image, which expnded to run spark jobs. i have used the official airflow-spark image from the doc
  -you can check this Repo for more info
  ```
  ```
  -Build command
  ```
  docker build -t airspark:4.0 .
  ```
3- Up the docker-compose file
```
docker-compose up -d
```

4- then you have to use pip to install cassandra driver inside spark nodes,
    BTW, you can expand the spark binami image to include cassandra driver.
```
  pip intsll cassandra-driver
```

5- then you have to install kafka API in your machine. to enable you use KafkaProducer, and Consumer.
```
pip install kafka-python
```
6- and finally create the kafka topic:
```
docker exec -it broker
kafka-topics --create --topic users --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
```
## Run the applcation
After following the prevous setup steps, you now ready to start streaming.
1- first way open airflow webserver UI and run the dag.
  ```
  http://localhost:8080/login/
  ```
  -user: airflow
  -password: airflow

2-you can use CMD to run the application
  - run the Producer:
  ```
  cd app
  python kafka_streaming_producer.py
  ```
  - use spark submit to run the spark Job
  ```
  docker exec -it spark-master bash
  cd app
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.0 spark.py
  ```



## Using "cqlsh" Cassandra Query Language Shell
Here you can use cqlsh to run your sql batch scripts on the data that loaded into Cassandra
 - At first go into cassandra container:
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
