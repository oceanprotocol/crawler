from time import sleep
import sys
import requests
from kafka import KafkaProducer

import json

from crawler.crawling.db.models.apInfo import ApartmentInfo

if __name__ == '__main__':
    apInfo = ApartmentInfo()

    apInfo.url  = "hha"
    print(json.dumps(apInfo.__dict__))