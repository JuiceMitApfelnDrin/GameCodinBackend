from get_databases_client import get_database
dbname = get_database()


collection_name = dbname["users"]

item_1 = {
    "_id": "U1IT00003",
    "username": "juicemitapfelndrin",
    "email": "juicemitapfelndrin@dings.com",
    "prefernces": "prefdings"
}
item_2 = {
    "_id": "U1IT00001",
    "username": "Gorn10",
    "email": "gorn10@dings.com",
    "prefernces": "prefdings"
}
item_3 = {
    "_id": "U1IT00002",
    "username": "Hydrazer",
    "email": "hydrazer@dings.com"
}
item_4 = {
    "_id": "U1IT00004",
    "username": "jutyve",
    "email": "jutyve@dings.com"
}

collection_name.insert_many([item_1, item_2, item_4, item_3])
