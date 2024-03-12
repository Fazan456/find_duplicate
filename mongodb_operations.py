from pymongo import MongoClient
from datetime import datetime

connection_string = '' #Add Mongodb uri
collections = [
   'collection_1,
   'collection_2'

]

def connect_to_mongodb():
    client = MongoClient(connection_string)
    database = client[db_name]
    return client, database

def close_mongodb_connection(client):
    client.close()

def get_duplicate_reference_ids():
    client, db = connect_to_mongodb()

    aggregation_results = {}
    for collection_name in collections:
        collection = db[collection_name]
        pipeline = [
    {
        "$group": {
            "_id": "$referenceId",
            "count": { "$sum": 1 },
            "ids": { "$addToSet": "$_id" },
            "dates": { "$addToSet": "$created_date" } 
        }
    },
    {
        "$match": {
            "count": { "$gt": 1 }
        }
    },
    {
        "$unwind": "$dates"  
    },
    {
        "$sort": {
            "_id": 1, 
            "dates": 1    #Add Aggregation Query to target specific field in all collections
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "count": { "$first": "$count" },
            "ids": { "$first": "$ids" },
            "dates": { "$push": "$dates" }  
        }
    },
    {
        "$project": {
            "_id": 1,
            "dates": { "$slice": ["$dates", { "$subtract": [{ "$size": "$dates" }, 1] }] }  
        }
    }
]


        duplicate_groups = list(collection.aggregate(pipeline))
        aggregation_results[collection_name] = duplicate_groups

    close_mongodb_connection(client)
    return aggregation_results
