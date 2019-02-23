#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: Perform queries against MongoDB
# USAge: python3 ./query_mongo.py

import pymongo
import os

mongodb_conn = os.environ.get('MONOGDB_CONN')
mongodb_client = pymongo.MongoClient(mongodb_conn)
mongo_db = mongodb_client["movies"]
mongo_collection = mongo_db["movieDetails"]


def create_indexes():
    mongo_collection.create_index([("title", pymongo.ASCENDING)])

    mongo_collection.create_index([("countries", pymongo.ASCENDING)])

    # mongo_collection.create_index([("title", pymongo.TEXT)])

    mongo_collection.create_index([("genres", pymongo.TEXT),
                                   ("title", pymongo.TEXT),
                                   ("plot", pymongo.TEXT)])


def find_documents(query, *sort, projection={'_id': 0, 'title': 1}):
    if sort:
        documents = mongo_collection \
            .find(query, projection) \
            .sort(*sort) \
            .limit(5)
    else:
        documents = mongo_collection \
            .find(query, projection) \
            .limit(5)

    print("----------\n")
    print("Parameters\n----------")
    # print(documents.explain())
    print("query: %s" % query)
    print("projection: %s" % projection)
    try:
        print("sort: %s" % sort)
    except TypeError:
        print("sort: %s" % "none")
    print("\nResults\n----------")
    print("document count: %s" % documents.count())
    for document in documents:
        if 'score' in document:
            document['score'] = round(document['score'], 2)
        print(document)


def count_documents():
    count = mongo_collection.count()

    print("----------\n")
    print("Parameters\n----------")
    # print(documents.explain())
    print("query: {}")
    print("\nResults\n----------")
    print("document count: %s" % count)


create_indexes()

# Query 1a: All Documents
find_documents({})

# Query 1b: Count Only
count_documents()

# Query 2: Exact Search
find_documents({'title': 'Star Wars: Episode V - The Empire Strikes Back'})

# Query 3: Search Phrase
find_documents({'title': {'$regex': r'\bstar wars\b', '$options': 'i'}})

# Query 4: Search Terms
# find_documents({'title': {'$regex': 'star|wars', '$options': 'i'}})
find_documents({'$text': {'$search': 'star wars',
                          '$language': 'en',
                          '$caseSensitive': False},
                'countries': 'USA'},
               [('score', {'$meta': 'textScore'})],
               projection={'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1})

# Query 5a: Multiple Search Terms
find_documents({'genres': {'$in': ['Adventure', 'Action', 'Western']}, 'countries': 'USA'},
               projection={'_id': 0, 'genres': 1, 'title': 1})

# Query 6
find_documents({'$text': {'$search': 'western action adventure',
                          '$language': 'en',
                          '$caseSensitive': False},
                'countries': 'USA'},
               [('score', {'$meta': 'textScore'})],
               projection={'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1})

# # Additional Unused Query Variations
# find_documents({'$text': {'$search': 'Star Wars: Episode V - The Empire Strikes Back',
#                           '$language': 'en',
#                           '$caseSensitive': False},
#                 'countries': 'USA'},
#                [('score', {'$meta': 'textScore'})],
#                projection={'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1})
# find_documents({'title': {'$regex': r'\bstar wars\b|\bstar trek\b', '$options': 'i'}})
#
# find_documents({'plot': {'$regex': r'\bwestern\b|\baction\b|\badventure\b', '$options': 'i'},
#                 'countries': 'USA'})
#
# find_documents({'plot': {'$regex': 'western|action|adventure', '$options': 'i'},
#                 'countries': 'USA'})
#
# find_documents({'title': {'$regex': r'\bstar\b|\bwars\b', '$options': 'i'}})
#
# find_documents({'$or': [{'title': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}},
#                         {'plot': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}},
#                         {'genres': {'$regex': r'\bwestern\b|\baction\b|\adventure\b', '$options': 'i'}}],
#                 'countries': 'USA'})
#
# find_documents({'$or': [{'title': {'$regex': 'western|action|adventure', '$options': 'i'}},
#                         {'plot': {'$regex': 'western|action|adventure', '$options': 'i'}},
#                         {'genres': {'$regex': 'western|action|adventure', '$options': 'i'}}],
#                 'countries': 'USA'})
