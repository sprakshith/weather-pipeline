from pymongo import MongoClient
from bson.objectid import ObjectId
from project_credentials.db_credentials import *


def get_database():
    db_url = f"mongodb+srv://{MONGO_DB_USER}:{PASSWORD}@{CLUSTER}.rd5qm6z.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(db_url)
    return client[DATABASE]


def create_object_id(_id):
    return ObjectId(_id)


if __name__ == "__main__":
    database = get_database()
    print("Connection Successful")
