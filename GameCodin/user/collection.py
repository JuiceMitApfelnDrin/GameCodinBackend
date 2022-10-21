import pymongo
from pymongo.collation import Collation, CollationStrength
from ..database import db_client

users_collection = db_client.get_collection("USERS") 
users_collection.create_index([
    ("username", pymongo.TEXT),
    ("email", pymongo.TEXT,)
], unique=True, collation=Collation(locale="en", strength=CollationStrength.SECONDARY))