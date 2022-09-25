from get_databases_client import get_database
dbname = get_database()


collection_name = dbname["users"]

item_1 = {
  "_id" : "U1IT00003",
  "username" : "juicemitapfelndrin",
  "email" : "juicemitapfelndrin@dings.com",
  "prefernces":"prefdings"
}

collection_name.insert_many([item_1])