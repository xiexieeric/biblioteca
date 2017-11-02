from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time
import json

while True:
	try:
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
		break
	except:
		time.sleep(1)
for message in consumer:
	new_listing = json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
	es.indices.refresh(index="listing_index")
