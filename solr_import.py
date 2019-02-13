#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: Add MongoDB collection of documents to Solr collection
# usage: python3 ./solr_import.py

import json
import os
import requests

solr_url = os.environ.get('SOLR_URL')
solr_collection = "movies"
data_file = "data/movieDetails.json"


def delete_all():
    # https://wiki.apache.org/solr/FAQ
    path = "/update"
    headers = {'Content-type': 'text/xml', 'charset': 'utf-8'}

    raw_data = "<delete><query>*:*</query></delete>"
    r = requests.post(solr_url + "/" + solr_collection + path, data=raw_data, headers=headers)
    print("delete status: ", r.status_code, r.reason)

    raw_data = "<commit/>"
    r = requests.post(solr_url + "/" + solr_collection + path, data=raw_data, headers=headers)
    print("commit status: ", r.status_code, r.reason)


def load_json():
    with open(data_file) as data:
        json_data = json.load(data)

    path = "/update/json/docs?commit=true"
    r = requests.post(solr_url + "/" + solr_collection + path, json=json_data)
    print("add all status: ", r.status_code, r.reason)


delete_all()
load_json()
