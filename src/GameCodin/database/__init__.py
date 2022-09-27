import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

CONNECTION_STRING = os.environ['DATABASE_CONNECTION_STRING']
client = MongoClient(CONNECTION_STRING, server_api=ServerApi('1'))