#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: Add MongoDB collection of documents to Solr collection
# usage: python3 ./mongo_to_solr.py

import json
import pymongo
import os
import requests
from bson.json_util import dumps

mongodb_conn = os.environ.get('MONGODB_CONN')
mongodb_client = pymongo.MongoClient(mongodb_conn)
mongo_db = mongodb_client["video"]
mongo_collection = mongo_db["movieDetails"]

solr_url = os.environ.get('SOLR_URL')
solr_collection = "movies"


# Read documents from JSON file
def get_documents():
    # https://www.w3schools.com/python/python_mongodb_query.asp
    mongo_query = {}
    documents = mongo_collection.find(mongo_query)
    return documents


# Add documents to Solr in bulk
def add_all():
    # https://lucene.apache.org/solr/guide/7_6/uploading-data-with-index-handlers.html#adding-multiple-json-documents
    documents = get_documents()

    path = "/update/json/docs?commit=true"

    print("documents to add: ", dumps(documents.count()))

    r = requests.post(solr_url + "/" + solr_collection + path, data=dumps(documents))
    print("add all status: ", r.status_code, r.reason, r.url, r.content)


# Add documents to Solr one at a time
def add_each():
    # https://lucene.apache.org/solr/guide/7_6/uploading-data-with-index-handlers.html#adding-multiple-json-documents

    documents = get_documents()
    path = "/update/json/docs?commit=true"
    print("documents to add: ", dumps(documents.count()))

    for document in documents:
        print(dumps(document))
        r = requests.post(solr_url + "/" + solr_collection + path, data=dumps(document))
        print("add all status: ", r.status_code, r.reason, r.url, r.content)


# Delete all documents in Solr
def delete_all():
    # https://wiki.apache.org/solr/FAQ
    path = "/update"
    headers = {'Content-type': 'text/xml', 'charset': 'utf-8'}

    raw_data = "<delete><query>*:*</query></delete>"
    r = requests.post(solr_url + "/" + solr_collection + path, data=raw_data, headers=headers)
    print("delete status: ", r.status_code, r.reason, r.url, r.content)

    raw_data = "<commit/>"
    r = requests.post(solr_url + "/" + solr_collection + path, data=raw_data, headers=headers)
    print("commit status: ", r.status_code, r.reason, r.url, r.content)


# def create_collection():
#     # ** THIS DOESN'T WORK **
#     # https://lucene.apache.org/solr/guide/7_6/collections-api.html
#     path = "/admin/collections?action=CREATE&name=" + solr_collection + \
#            "&collection.configName=_default&&numShards=2&replicationFactor=1&wt=xml"
#     r = requests.get(solr_url + path)
#     print("commit status: ", r.status_code, r.reason, r.content)
#
#     path = "/config"
#     data = {'set-user-property': {'update.autoCreateFields': 'false'}}
#     r = requests.post(solr_url + "/" + solr_collection + path, json=data)
#     print("commit status: ", r.status_code, r.reason, r.url, r.content)


# Load JSON file documents into Solr
def load_json():
    with open('data/movieDetails.json') as json_data:
        json_data = json.load(json_data)

    path = "/update/json/docs?commit=true"

    # print("documents to add: ", dumps(json_data))

    r = requests.post(solr_url + "/" + solr_collection + path, data=dumps(json_data))
    print("add all status: ", r.status_code, r.reason)


# Change schema items to multiValued = falses
def multi_value_false():
    path = "/schema"
    json_data = "{\"replace-field\":{\"name\":\"title\",\"type\":\"text_general\",\"multiValued\":false}," \
                "\"replace-field\":{\"name\":\"plot\",\"type\":\"text_general\",\"multiValued\":false}}"

    r = requests.post(solr_url + "/" + solr_collection + path, data=json_data)
    print("add all status: ", r.status_code, r.reason)


# create_collection()
multi_value_false()
# delete_all()
# load_json()
# add_all()
# add_each()
