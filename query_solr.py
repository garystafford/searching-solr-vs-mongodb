#!/usr/bin/env python3
#
# author: Gary A. Stafford
# site: https://programmaticponderings.com
# license: MIT License
# purpose: Perform searches against a Solr index
# usage: python3 ./query_solr.py

import pysolr
import os
from bson.json_util import dumps

solr_url = os.environ.get('SOLR_URL')

solr_collection = "movies"
solr = pysolr.Solr(solr_url + "/" + solr_collection)


# Solr's default Query Parser (aka lucene parser)
def solr_search(q, args):
    results = solr.search(q, **args)

    print("---")
    print("find_title_contains q: %s" % q)
    print("find_title_contains hits: %s" % results.hits)
    print("find_title_contains qtime (ms): %s" % results.qtime)
    print("find_title_contains docs: %s" % dumps(results.docs))


# More Like This Query Parser (MLTQParser) example
def more_like_this_query_parser(q, mltfl):
    results = solr.more_like_this(q, mltfl)
    # {"fl": "id plot title genres actors director score", "rows": "5"}
    print("---")
    print("more_like_this q: %s" % q)
    print("more_like_this hits: %s" % results.hits)
    print("more_like_this qtime (ms): %s" % results.qtime)
    print("more_like_this docs: %s" % dumps(results.docs))


# score is always 1.0 (default)
solr_search("*:*", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

solr_search("\"Star Wars: Episode V - The Empire Strikes Back\"", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

solr_search("\"star wars\"", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

solr_search("star wars", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

solr_search("*star* *wars*", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

solr_search("\"star wars\" OR \"star trek\"", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

solr_search("western action adventure", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

# why we can't add 'adventure' as a stop word
solr_search("\"adventure\"", {
    "defType": "lucene",
    "fl": "id title score",
    "rows": "5"})

# Extended DisMax (eDismax) Query Parser - Basic example, no boost
solr_search("western action adventure", {
    "defType": "edismax",
    "qf": "plot title genres",
    "fl": "id title genres score",
    "rows": "5"})

solr_search("*western* *action* *adventure*", {
    "defType": "edismax",
    "qf": "plot title genres",
    "fl": "id title genres score",
    "rows": "5"})

# eDismax - Basic example, multiple search terms
solr_search("*western* *action* *adventure*", {
    "defType": "edismax",
    "qf": "plot title genres actors director",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

solr_search("actors:\"John Wayne\" AND western action adventure", {
    "defType": "edismax",
    "qf": "plot title genres actors director",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

solr_search("western action adventure with John Wayne", {
    "defType": "edismax",
    "qf": "plot title genres actors director",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

solr_search("western action adventure +\"John Wayne\"", {
    "defType": "edismax",
    "qf": "plot title genres actors director",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

# eDismax - Boosted fields
solr_search("western action adventure", {
    "defType": "edismax",
    "qf": "plot title^2.0 genres^3.0",
    "fl": "id title genres score",
    "rows": "5"})

solr_search("classic western action adventure adventure", {
    "defType": "edismax",
    "qf": "plot title^2.0 genres^3.0",
    "fl": "id title genres score",
    "rows": "5"})

# eDismax - Boost results that have a field that matches a specific value
solr_search("classic western action adventure adventure", {
    "defType": "edismax",
    "qf": "plot title^2.0 genres^3.0",
    "bq": "genres:western^5.0",
    "fl": "id title genres score",
    "rows": "5"})

# More Like This Query Parser (MLTQParser) example
mlt_id = "07776f22-e4db-463e-a6c0-50f692e30838"

mlt_qf = "director writers"
solr_search("{!mlt qf=\"%s\" mintf=1 mindf=1}%s" % (mlt_qf, mlt_id), {
    "defType": "lucene",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

mlt_qf = "actors"
solr_search("{!mlt qf=\"%s\" mintf=1 mindf=1}%s" % (mlt_qf, mlt_id), {
    "defType": "lucene",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

mlt_qf = "genres"
solr_search("{!mlt qf=\"%s\" mintf=1 mindf=1}%s" % (mlt_qf, mlt_id), {
    "defType": "lucene",
    "fl": "id plot title genres actors director score",
    "rows": "5"})

# more_like_this_query_parser("id:07776f22-e4db-463e-a6c0-50f692e30838", "genres")
