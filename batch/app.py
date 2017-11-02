from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time
import json

while True:
	try:
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
		request_body = {
		    "settings" : {
		        "number_of_shards": 1,
		        "number_of_replicas": 0
		    }
		}
		es.indices.create(index = 'listing_index', body = request_body, ignore = 400)
		break
	except:
		time.sleep(1)

for message in consumer:
	new_listing = json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
	es.indices.refresh(index="listing_index")
