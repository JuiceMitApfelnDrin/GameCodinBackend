from get_databases_client import get_database
dbname = get_database()

collection_name = dbname["users"]

item_details = collection_name.find()
for item in item_details:
    print(item)
