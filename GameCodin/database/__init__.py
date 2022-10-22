__all__ = ["db_client"]

from ..env import load_dotenv

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final

database_name: Final  = "GameCodin"
connection_string: Final = load_dotenv()['DATABASE_CONNECTION_STRING']
db_client: Final = MongoClient(connection_string, server_api=ServerApi('1'))[database_name]