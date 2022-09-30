__all__ = ["db_client"]

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final
from dotenv import load_dotenv
load_dotenv('./env/.env')

os.environ['DATABASE_CONNECTION_STRING'] = "mongodb+srv://JuiceMitApfelnDrin:GOlw5Vays0rpK3Iy@gamecodin.kq8ct9s.mongodb.net/?retryWrites=true&w=majority"

database_name="GameCodin"
connection_string: Final = os.environ['DATABASE_CONNECTION_STRING']
db_client: Final = MongoClient(connection_string, server_api=ServerApi('1'))[database_name]