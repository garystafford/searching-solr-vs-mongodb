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


def find_documents(query, projection={'_id': 0, 'title': 1}, sort=[('title', pymongo.ASCENDING)]):
    documents = mongo_collection \
        .find(query, projection) \
        .sort(sort) \
        .limit(5)

    print("----------\n")
    print("Parameters\n----------")
    # print(documents.explain())
    print("query: %s" % query)
    print("projection: %s" % projection)
    print("sort: %s" % sort)
    print("\nResults\n----------")
    print("document count: %s" % documents.count())
    for document in documents:
        if 'score' in document:
            document['score'] = round(document['score'], 2)
        print(document)


# create_indexes()

# Query 1
find_documents(query={})

# Query 2
find_documents(query={'title': 'Star Wars: Episode V - The Empire Strikes Back'})

# Query 3
find_documents(query={'title': {'$regex': r'\bstar wars\b', '$options': 'i'}})

# Query 4
find_documents(query={'title': {'$regex': r'\bstar\b|\bwars\b', '$options': 'i'}})

# Query 5
find_documents(query={'title': {'$regex': 'star|wars', '$options': 'i'}})

# Query #6
find_documents(query={'genres': {'$in': ['Western', 'Action', 'Adventure']}, 'countries': 'USA'})

# Query 7
find_documents(query={'$or': [{'title': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}},
                              {'plot': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}},
                              {'genres': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}}],
                      'countries': 'USA'})

# Query 8
find_documents(query={'$or': [{'title': {'$regex': 'western|action|adventure', '$options': 'i'}},
                              {'plot': {'$regex': 'western|action|adventure', '$options': 'i'}},
                              {'genres': {'$regex': 'western|action|adventure', '$options': 'i'}}],
                      'countries': 'USA'})

# Query 9
find_documents(query={'$text': {'$search': 'western action adventure',
                                '$language': 'en',
                                '$caseSensitive': False},
                      'countries': 'USA'})

find_documents(query={'$text': {'$search': 'western action adventure',
                                '$language': 'en',
                                '$caseSensitive': False},
                      'countries': 'USA'},
               projection={'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1},
               sort=[('score', {'$meta': 'textScore'})])

find_documents(query={'$text': {'$search': 'Star Wars: Episode V - The Empire Strikes Back',
                                '$language': 'en',
                                '$caseSensitive': False},
                      'countries': 'USA'},
               projection={'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1},
               sort=[('score', {'$meta': 'textScore'})])

# # Unused #1
# find_documents(query={'title': {'$regex': r'\bstar wars\b|\bstar trek\b', '$options': 'i'}})
#
# # Unused #2
# find_documents(query={'plot': {'$regex': r'\bwestern\b|\baction\b|\badventure\b', '$options': 'i'},
#                       'countries': 'USA'})
#
# # Unused #3
# find_documents(query={'plot': {'$regex': 'western|action|adventure', '$options': 'i'},
#                       'countries': 'USA'})
