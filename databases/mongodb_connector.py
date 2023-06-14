from pymongo import MongoClient
from project_credentials.db_credentials import *


def get_database():
    db_url = f"mongodb+srv://{MONGO_DB_USER}:{PASSWORD}@{CLUSTER}.rd5qm6z.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(db_url)
    return client[DATABASE]


if __name__ == "__main__":
    database = get_database()
    print("Connection Successful")
