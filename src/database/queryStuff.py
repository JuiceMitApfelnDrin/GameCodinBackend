

def ding():
    dbname = Database.get_database()

    collection_name = dbname["users"]

    item_details = collection_name.find()

    return item_details
