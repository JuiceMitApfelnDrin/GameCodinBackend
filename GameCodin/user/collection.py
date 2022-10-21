import pymongo
from ..database import db_client

users_collection = db_client.get_collection("USERS") 
users_collection.create_index([("username", pymongo.TEXT),("email", pymongo.TEXT)], unique=True)