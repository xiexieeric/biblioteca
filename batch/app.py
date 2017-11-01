from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time

while True:
	try:
		consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
		break
	except:
		time.sleep(1)
for message in consumer:
	new_listing = {'title': null}