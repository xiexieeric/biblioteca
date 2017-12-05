from kafka import KafkaConsumer
import time
import json

while True:
	try:
		consumer = KafkaConsumer('new-click-topic', group_id='click-indexer', bootstrap_servers=['kafka:9092'])
		request_body = {
		    "settings" : {
		        "number_of_shards": 1,
		        "number_of_replicas": 0
		    }
		}
		break
	except:
		time.sleep(1)

for message in consumer:
	new_click = json.loads((message.value).decode('utf-8'))
	with open("/app/spark/data/access.log", "a") as myfile:
   		myfile.write(new_click['user']+'\t'+new_click['listing'])
