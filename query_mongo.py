#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: Perform queries against MongoDB
# usage: python3 ./query_mongo.py

import pymongo
import os

mongodb_conn = os.environ.get('MONOGDB_CONN')
mongodb_client = pymongo.MongoClient(mongodb_conn)
mongo_db = mongodb_client["movies"]
mongo_collection = mongo_db["movieDetails"]


def create_indexes():
    mongo_collection.create_index([("title", pymongo.ASCENDING)])

    mongo_collection.create_index([("genres", pymongo.TEXT),
                                   ("title", pymongo.TEXT),
                                   ("plot", pymongo.TEXT)])


def find_documents(query, projection={'title': 1}, sort=[('title', pymongo.ASCENDING)]):
    # https://docs.mongodb.com/manual/reference/method/db.collection.find/

    documents = mongo_collection \
        .find(query, projection) \
        .sort(sort) \
        .limit(5)

    print("---")
    print("query: %s" % query)
    print("projection: %s" % projection)
    print("count: %s" % documents.count())
    for document in documents:
        print(document)


def search_documents(query, projection={'score': {'$meta': 'textScore'}, 'title': 1},
                     sort=[('score', {'$meta': 'textScore'})]):
    # https://docs.mongodb.com/manual/text-search/

    documents = mongo_collection \
        .find(query, projection) \
        .sort(sort) \
        .limit(5)

    print("---")
    print("query: %s" % query)
    print("projection: %s" % projection)
    print("count: %s" % documents.count())
    for document in documents:
        print(document)


create_indexes()

find_documents({})

find_documents({'title': 'Star Wars: Episode V - The Empire Strikes Back'})

find_documents({'title': {'$regex': r'\bstar wars\b', '$options': 'i'}})

find_documents({'title': {'$regex': r'\bstar\b|\bwars\b', '$options': 'i'}})

find_documents({'title': {'$regex': 'star|wars', '$options': 'i'}})

find_documents({'title': {'$regex': r'\bstar wars\b|\bstar trek\b', '$options': 'i'}})

find_documents({'genres': {'$in': ['Western', 'Action', 'Adventure']}})

find_documents({'plot': {'$regex': 'western|action|adventure', '$options': 'i'}})

find_documents({'$or': [{'title': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}},
                        {'plot': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}},
                        {'genres': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}}]})

find_documents({'$or': [{'title': {'$regex': 'western|action|adventure', '$options': 'i'}},
                        {'plot': {'$regex': 'western|action|adventure', '$options': 'i'}},
                        {'genres': {'$regex': 'western|action|adventure', '$options': 'i'}}]})

find_documents({'$text': {'$search': 'western action adventure'}})

search_documents({'$text': {'$search': 'western action adventure'}})
