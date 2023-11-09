import uuid
import requests
import time
import logging
import json
from kafka import KafkaProducer


########## Streaming the data From results-API ############
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
    bootstrap_server_name = ["localhost:9092"] #produce to this host
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
streaming_data()