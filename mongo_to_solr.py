#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: ETL - Import MongoDB collection of documents to Solr index
# usage: python3 ./mongo_to_solr.py

import pymongo
import os
import requests
from bson.json_util import dumps

mongodb_conn = os.environ.get('MONGODB_CONN')
mongodb_client = pymongo.MongoClient(mongodb_conn)
mongo_db = mongodb_client['video']
mongo_collection = mongo_db['movieDetails']
solr_url = os.environ.get('SOLR_URL')
solr_collection = 'movies'


def main():
    get_documents
    add_all()


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

    path = '/update/json/docs?commit=true'

    print('documents to add: ', dumps(documents.count()))

    r = requests.post(solr_url + '/' + solr_collection + path, data=dumps(documents))
    print('add all status: ', r.status_code, r.reason, r.url, r.content)


# Add documents to Solr one at a time
def add_each():
    # https://lucene.apache.org/solr/guide/7_6/uploading-data-with-index-handlers.html#adding-multiple-json-documents

    documents = get_documents()
    path = '/update/json/docs?commit=true'
    print('documents to add: ', dumps(documents.count()))

    for document in documents:
        print(dumps(document))
        r = requests.post(solr_url + '/' + solr_collection + path, data=dumps(document))
        print('add all status: ', r.status_code, r.reason, r.url, r.content)


# TODO - Not working correctly
def create_collection():
    # https://lucene.apache.org/solr/guide/7_6/collections-api.html
    path = '/admin/collections?action=CREATE&name=' + solr_collection + \
           '&collection.configName=_default&&numShards=2&replicationFactor=1&wt=xml'
    r = requests.get(solr_url + path)
    print('commit status: ', r.status_code, r.reason, r.content)

    path = '/config'
    data = {'set-user-property': {'update.autoCreateFields': 'false'}}
    r = requests.post(solr_url + '/' + solr_collection + path, json=data)
    print('commit status: ', r.status_code, r.reason, r.url, r.content)


# Change schema items to multiValued = false
def multi_value_false():
    path = '/schema'
    json_data = '{"replace-field":{"name":"title","type":"text_general","multiValued":false},' \
                '"replace-field":{"name":"plot","type":"text_general","multiValued":false}}'

    r = requests.post(solr_url + '/' + solr_collection + path, data=json_data)
    print('add all status: ', r.status_code, r.reason)


if __name__ == "__main__":
    main()
