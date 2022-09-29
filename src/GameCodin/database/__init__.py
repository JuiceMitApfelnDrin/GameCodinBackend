__all__ = ["db_client"]

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final
from dotenv import load_dotenv
load_dotenv('./env/.env')

database_name="GameCodin"
connection_string: Final = os.environ['DATABASE_CONNECTION_STRING']
db_client: Final = MongoClient(connection_string, server_api=ServerApi('1'))[database_name]