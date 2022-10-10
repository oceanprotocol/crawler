from pymongo import MongoClient
import os

client = MongoClient(os.environ["MONGO_CON"])

mongo_client = client[os.environ["DB_NAME"]]
