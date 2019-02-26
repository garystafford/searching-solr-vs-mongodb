#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: Index the collection of movie documents to Solr
# usage: python3 ./solr_index_movies.py

import json
import os
import requests

solr_url = os.environ.get('SOLR_URL')
solr_collection = 'movies'
data_file = 'data/movieDetails.json'


def main():
    delete_all_documents()
    load_json_file_to_solr()
    multi_value_false()
    delete_all_documents()
    load_json_file_to_solr()
    get_document_count()


def delete_all_documents():
    # https://wiki.apache.org/solr/FAQ
    path = '/update'
    headers = {'Content-type': 'text/xml', 'charset': 'utf-8'}

    raw_data = '<delete><query>*:*</query></delete>'
    r = requests.post(solr_url + '/' + solr_collection + path, data=raw_data, headers=headers)
    print('Delete all documents: ', r.status_code, r.reason)

    raw_data = '<commit/>'
    r = requests.post(solr_url + '/' + solr_collection + path, data=raw_data, headers=headers)
    print('Commit delete: ', r.status_code, r.reason)


def load_json_file_to_solr():
    with open(data_file) as data:
        json_data = json.load(data)
        json_data = add_id(json_data)

    path = '/update/json/docs?commit=true'
    r = requests.post(solr_url + '/' + solr_collection + path, json=json_data)
    print('Bulk add all documents: ', r.status_code, r.reason)


# Add Solr ID field by copying MongoDB ID field
def add_id(json_data):
    for document in json_data:
        document['id'] = document['_id']['$oid']
    return json_data


def multi_value_false():
    path = '/schema'
    json_data = '{"replace-field":{"name":"title","type":"text_en","multiValued":false},' \
                '"replace-field":{"name":"plot","type":"text_en","multiValued":false},' \
                '"replace-field":{"name":"genres","type":"text_en","multiValued":true}}'

    r = requests.post(solr_url + '/' + solr_collection + path, data=json_data)
    print('Modify schema: ', r.status_code, r.reason)


def get_document_count():
    path = '/select?q=*:*&rows=0'
    r = requests.get(solr_url + '/' + solr_collection + path)
    print('Document count: ', r.status_code, r.reason, r.text)


if __name__ == "__main__":
    main()
