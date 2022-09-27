__all__ = ["client"]

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final

connection_string: Final = os.environ['DATABASE_CONNECTION_STRING']
client: Final = MongoClient(connection_string, server_api=ServerApi('1'))