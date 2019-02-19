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
def solr_search(q, **kwargs):
    results = solr.search(q, **kwargs)

    print("----------\n")
    print("Parameters\n----------")
    print("q: %s" % q)
    print("kwargs: %s" % kwargs)
    print("\nResults\n----------")
    print("document count: %s" % results.hits)
    print("qtime (ms): %s" % results.qtime)
    # print("docs: %s" % dumps(results.docs))
    for document in results.docs:
        if 'score' in document:
            document['score'] = round(document['score'], 2)
        print(document)


# More Like This Query Parser (MLTQParser) example
def more_like_this_query_parser(q, mltfl):
    results = solr.more_like_this(q, mltfl)

    print("----------\n")
    print("Parameters\n----------")
    print("q : %s" % q)
    print("mltfl: %s" % mltfl)
    print("\nResults\n----------")
    print("document count: %s" % results.hits)
    print("qtime (ms): %s" % results.qtime)
    print("docs: %s" % dumps(results.docs))


# Query 1
solr_search("*:*", **{
    "defType": "lucene",
    "fl": "title score",
    "sort": "title asc",
    "rows": "5"})

# Query 2
solr_search("\"Star Wars: Episode V - The Empire Strikes Back\"", **{
    "defType": "lucene",
    "df": "title",
    "fl": "title score"})

# Query 3
solr_search("\"star wars\"", **{
    "defType": "lucene",
    "df": "title",
    "fl": "title score"})

# Query 4
solr_search("star wars", **{
    "defType": "lucene",
    "fq": "countries: USA",
    "df": "title",
    "fl": "title score",
    "rows": "5"})

# Query 5
solr_search("(adventure action western)", **{
    "defType": "lucene",
    "fq": "countries: USA",
    "df": "genres",
    "fl": "title genres score",
    "rows": "5"})

# Query 5: Alternate - Require Western
solr_search("(adventure action +western)", **{
    "defType": "lucene",
    "fq": "countries: USA",
    "df": "genres",
    "fl": "title genres score",
    "rows": "5"})

# Extended DisMax (eDismax) Query Parser - Basic example, no boost
# Query 6
solr_search("adventure action western", **{
    "defType": "edismax",
    "fq": "countries: USA",
    "qf": "plot title genres",
    "fl": "title genres score",
    "rows": "10"})

# Query 6: Alternate - Require/Prohibit
solr_search("adventure action +western -romance cowboy", **{
    "defType": "edismax",
    "fq": "countries: USA",
    "qf": "plot title genres",
    "fl": "title genres score",
    "rows": "5"})

# Query 7: The Movie Dilemma
solr_search("A cowboys movie", **{
    "defType": "edismax",
    "fq": "countries: USA",
    "qf": "plot title genres",
    "fl": "title genres score",
    "rows": "10"})

# Query 7: Alternate - Stop Words (simulation)
solr_search("The Lego Movie -movie", **{
    "defType": "edismax",
    "fq": "countries: USA",
    "qf": "plot title genres",
    "fl": "title genres score",
    "rows": "10"})

# Query 7: Alternate 2 - Negative Boost
solr_search("A cowboys movie", **{
    "defType": "edismax",
    "fq": "countries: USA",
    "qf": "plot title genres",
    "bq": "title:movie^-2.0",
    "fl": "title genres score",
    "rows": "10"})

# # eDismax - Basic example, multiple search terms
# # Query 8
# solr_search("actors:\"John Wayne\" AND western action adventure", **{
#     "defType": "edismax",
#     "qf": "plot title genres actors director",
#     "fl": "id plot title genres actors director score",
#     "rows": "5"})
#
# # Query 9
# solr_search("western action adventure with John Wayne", **{
#     "defType": "edismax",
#     "qf": "plot title genres actors director",
#     "fl": "id plot title genres actors director score",
#     "rows": "5"})
#
# solr_search("western action adventure +\"John Wayne\"", **{
#     "defType": "edismax",
#     "qf": "plot title genres actors director",
#     "fl": "id plot title genres actors director score",
#     "rows": "5"})
#
# # eDismax - Boosted fields
# solr_search("western action adventure", **{
#     "defType": "edismax",
#     "qf": "plot title^2.0 genres^3.0",
#     "fl": "title genres score",
#     "rows": "5"})
#
# solr_search("classic western action adventure adventure", **{
#     "defType": "edismax",
#     "qf": "plot title^2.0 genres^3.0",
#     "fl": "title genres score",
#     "rows": "5"})
#
# # eDismax - Boost results that have a field that matches a specific value
# solr_search("classic western action adventure adventure", **{
#     "defType": "edismax",
#     "qf": "plot title^2.0 genres^3.0",
#     "bq": "genres:western^5.0",
#     "fl": "title genres score",
#     "rows": "5"})
#
# # More Like This Query Parser (MLTQParser) example
# mlt_id = "07776f22-e4db-463e-a6c0-50f692e30838"
#
# mlt_qf = "director writers"
# solr_search("{!mlt qf=\"%s\" mintf=1 mindf=1}%s" % (mlt_qf, mlt_id), **{
#     "defType": "lucene",
#     "fl": "id plot title genres actors director score",
#     "rows": "5"})
#
# mlt_qf = "actors"
# solr_search("{!mlt qf=\"%s\" mintf=1 mindf=1}%s" % (mlt_qf, mlt_id), **{
#     "defType": "lucene",
#     "fl": "id plot title genres actors director score",
#     "rows": "5"})
#
# mlt_qf = "genres"
# solr_search("{!mlt qf=\"%s\" mintf=1 mindf=1}%s" % (mlt_qf, mlt_id), **{
#     "defType": "lucene",
#     "fl": "id plot title genres actors director score",
#     "rows": "5"})

# more_like_this_query_parser("id:07776f22-e4db-463e-a6c0-50f692e30838", "genres")

# # Unused #1
# solr_search("\"star wars\" OR \"star trek\"", **{
#     "defType": "lucene",
#     "df": "title",
#     "fl": "title score",
#     "rows": "5"})
#
# why we can't add 'adventure' as a stop word
# # Unused #4
# solr_search("\"adventure\"", **{
#     "defType": "lucene",
#     "df": "title",
#     "fl": "title score",
#     "rows": "5"})
# Query 7
# solr_search("*western* *action* *adventure*", **{
#     "defType": "edismax",
#     "fq": "countries: USA",
#     "qf": "plot title genres",
#     "fl": "title genres score",
#     "rows": "5"})
