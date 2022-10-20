__all__ = ["db_client", "Collection"]

from ..env import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final
from .collection import Collection

database_name: Final  = "GameCodin"
connection_string: Final = os.environ['DATABASE_CONNECTION_STRING']
db_client: Final = MongoClient(connection_string, server_api=ServerApi('1'))[database_name]