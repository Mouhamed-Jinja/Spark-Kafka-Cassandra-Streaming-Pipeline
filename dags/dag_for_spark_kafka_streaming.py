from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import uuid
import requests
import time
import logging
import json
from kafka import KafkaProducer

def get_data():
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])}, {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data



######### Start Streaming to Kafka #########
def streaming_data():
    curr_time = time.time()
    topic_name = "users"
    bootstrap_server_name = ['broker:29092'] #produce to this host
    producer = KafkaProducer(bootstrap_servers =bootstrap_server_name , max_block_ms = 5000)
    while True:
            if time.time() > curr_time + 120: #1 minute
                break
            try:
                reponse = get_data()
                reponse = format_data(reponse)
                #res_json = json.dumps(res, indent=3)
                #print(res_json)
                print("Producing...")
                producer.send(topic=topic_name, value= json.dumps(reponse).encode('utf-8'))
                
            except Exception as e:
                logging.error(f'An error occured: {e}')
                continue


default_args = {
    'owner': 'younies',
    'retries': 5,
    'retry_delay': timedelta(seconds=60),
    'start_date': datetime(2023, 11, 9),
    'schedule_interval': '0 0 * * *',  # Run daily at midnight
}

with DAG(
    'dag_for_spark_kafka_cassandra_streaming14',
    default_args=default_args,
    catchup=False,
) as dag:

    stream_from_API_to_kafka = PythonOperator(
        task_id='kafka_streaming',
        python_callable=streaming_data
    )
    
    spark_stream_to_cassandra= BashOperator(
        task_id = "spark_streaming",
        bash_command = 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.0 /opt/airflow/spark/app/spark.py'
    )
    

stream_from_API_to_kafka
spark_stream_to_cassandra