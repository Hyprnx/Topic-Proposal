from pymongo import MongoClient
from pymongo.database import Database

def connect_to_database():
    host = 'localhost'
    port = 27017
    client = MongoClient(host, port)
    db = client.database
    if not isinstance(db, Database):
        raise ConnectionError("Connection failed, respond is not a MongoDB Database instance")
    return db
