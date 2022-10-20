import pymongo
from database import db_client

puzzle_collection = db_client.create_collection("puzzle")
puzzle_collection.create_index([("title", pymongo.TEXT)], unique=True)