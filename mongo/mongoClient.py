from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
import os
config = dotenv_values("../.env.local")
# client = MongoClient(os.environ['MONGO_CON'])
#
# db = client[os.environ["DB_NAME"]]
client = MongoClient(config['MONGO_CON'])

db = client[config["DB_NAME"]]

# db = client[config["DB_NAME"]]
#
# print(config['MONGO_CON'])
# client = MongoClient(config['MONGO_CON'])
#
# db = client[config["DB_NAME"]]
#
# class MongoClient:
#     def __init__(self):
#         self.client = MongoClient(config['MONGO_CON'])
#         self.db  = self.client[config["DB_NAME"]]
#         print("Connected to the MongoDB database!")