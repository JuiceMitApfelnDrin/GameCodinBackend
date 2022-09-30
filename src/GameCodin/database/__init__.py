__all__ = ["db_client"]

from email.mime import base
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Final

# TODO:
# It doesn't make sense to do this in database because its not the only part
# that will need to load .env, but doesn't make sense to load it in main either
# because we might need to test parts of the backends.
# The solution is to put it __init__.py in ../env and do from .. import env
# That will make sure that we load them only once, also remove the need to use
# find the absolute path.
from dotenv import load_dotenv
envpath = os.path.abspath(os.path.join(os.path.dirname(__file__),'../env/.env'))
load_dotenv(envpath)

database_name="GameCodin"
connection_string: Final = os.environ['DATABASE_CONNECTION_STRING']
db_client: Final = MongoClient(connection_string, server_api=ServerApi('1'))[database_name]