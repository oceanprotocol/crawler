from pymongo import MongoClient
import os

client = MongoClient(os.environ["MONGO_CON"])

mongoClient = client[os.environ["DB_NAME"]]
