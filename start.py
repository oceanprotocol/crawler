from time import sleep
import sys
import requests
from kafka import KafkaProducer

import json
spiderFlow = ['getCondosSpider', 'getOffersSpider', 'getOfferDetailsSpider']
initialJobId = None
import logging


def _kafka_success( response):
    '''
    Callback for successful send
    '''
    logging.error("Sent message to Kafka")


def _kafka_failure( response):
    '''
    Callback for failed send
    '''
    logging.error(response)
    logging.error("Failed to send message to Kafka")
    # self._spawn_kafka_connection_thread()

if __name__ == '__main__':
    logging.error("HI")
    try:
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                         value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                                         retries=3,
                                         api_version=(0, 10, 1),
                                         linger_ms=25,
                                         buffer_memory=4 * 1024 * 1024)
        json_i = '{"appid": "ui_service", "uuid": "2f98e5495a2f", "stats": "kafka-monitor"}'

        future = producer.send('demo.incoming',
                                     json_i)
        future.add_callback(_kafka_success)
        future.add_errback(_kafka_failure)
        logging.error('YOO')
        record_metadata = future.get(timeout=10)
        logging.error(record_metadata)
    except Exception as e:
        logging.error(e)
        logging.error('Watch out!')