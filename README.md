# Searching with Apache Solr

Materials for workshop on comparing searching with Apache Solr versus querying in MongoDB: 'Your Database is not a Search Engine'.

Movie data used in demo publicly available from MongoDB: [Setup and Import the Data](https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data)

## Set-up Instructions

Assuming you have an existing MongoDB and Solr instances:

-   Import JSON data to MongoDB (command below)
-   Create Solr `movies` collection (command below)
-   Import JSON data to Solr (Python script: `solr_import.py`)
-   Set (2) environment variables (commands below)
-   Run `query_mongo.py` and `query_solr.py` query scripts

## Useful Commands

Create Solr `movies` collection

```bash
solr-7.6.0/bin/solr create -c movies -s 2 -rf 2
```

Update environment variables with your own values and set

```bash
export SOLR_URL="http://{{ host }}:8983/solr"
export MONOGDB_CONN="mongodb+srv://{{ user }}:{{ password }}@{{ host }}/movies"
```

Import `movieDetails_mongo.json` JSON data to MongoDB

```bash
mongoimport \
  --uri $MONOGDB_CONN \
  --collection "movieDetails" \
  --drop --file "data/movieDetails_mongo.json"
```

Run scripts

```bash
time python3 ./query_mongo.py
time python3 ./query_solr.py

```

## Output from Solr Searches

Actually documents are not shown for brevity.

```text
---
solr_search q: *:*
solr_search hits: 2250
solr_search qtime (ms): 3
---
solr_search q: "Star Wars: Episode V - The Empire Strikes Back"
solr_search hits: 1
solr_search qtime (ms): 2
---
solr_search q: "star wars"
solr_search hits: 6
solr_search qtime (ms): 1
---
solr_search q: star wars
solr_search hits: 15
solr_search qtime (ms): 1
---
solr_search q: *star* *wars*
solr_search hits: 20
solr_search qtime (ms): 3
---
solr_search q: "star wars" OR "star trek"
solr_search hits: 11
solr_search qtime (ms): 1
---
solr_search q: western action adventure
solr_search hits: 24
solr_search qtime (ms): 1
---
solr_search q: "adventure"
solr_search hits: 11
solr_search qtime (ms): 1
---
solr_search q: western action adventure
solr_search hits: 24
solr_search qtime (ms): 1
---
solr_search q: *western* *action* *adventure*
solr_search hits: 452
solr_search qtime (ms): 19
---
solr_search q: actors:"John Wayne" AND western action adventure
solr_search hits: 3
solr_search qtime (ms): 2
---
solr_search q: western action adventure with John Wayne
solr_search hits: 793
solr_search qtime (ms): 2
---
solr_search q: western action adventure +"John Wayne"
solr_search hits: 4
solr_search qtime (ms): 1
---
solr_search q: western action adventure
solr_search hits: 434
solr_search qtime (ms): 2
---
solr_search q: classic western action adventure adventure
solr_search hits: 438
solr_search qtime (ms): 2
---
solr_search q: classic western action adventure adventure
solr_search hits: 438
solr_search qtime (ms): 1
---
solr_search q: {!mlt qf="director writers" mintf=1 mindf=1}07776f22-e4db-463e-a6c0-50f692e30838
solr_search hits: 53
solr_search qtime (ms): 7
---
solr_search q: {!mlt qf="actors" mintf=1 mindf=1}07776f22-e4db-463e-a6c0-50f692e30838
solr_search hits: 77
solr_search qtime (ms): 5
---
solr_search q: {!mlt qf="genres" mintf=1 mindf=1}07776f22-e4db-463e-a6c0-50f692e30838
solr_search hits: 440
solr_search qtime (ms): 4
```

## Output from MongoDB Queries

Actually documents are not shown for brevity.

```text
---
query: {}
projection: {'title': 1}
count: 2250
---
query: {'title': 'Star Wars: Episode V - The Empire Strikes Back'}
projection: {'title': 1}
count: 1
---
query: {'title': {'$regex': '\\bstar wars\\b', '$options': 'i'}}
projection: {'title': 1}
count: 6
---
query: {'title': {'$regex': '\\bstar\\b|\\bwars\\b', '$options': 'i'}}
projection: {'title': 1}
count: 15
---
query: {'title': {'$regex': 'star|wars', '$options': 'i'}}
projection: {'title': 1}
count: 20
---
query: {'title': {'$regex': '\\bstar wars\\b|\\bstar trek\\b', '$options': 'i'}}
projection: {'title': 1}
count: 11
---
query: {'genres': {'$in': ['Western', 'Action', 'Adventure']}}
projection: {'title': 1}
count: 410
---
query: {'plot': {'$regex': 'western|action|adventure', '$options': 'i'}}
projection: {'title': 1}
count: 53
---
query: {'$or': [{'title': {'$regex': '\\bwestern\\b|\\baction\\b|\\adventure\\b', '$options': 'i'}}, {'plot': {'$regex': '\\bwestern\\b|\\baction\\b|\\adventure\\b', '$options': 'i'}}, {'genres': {'$regex': '\\bwestern\\b|\\baction\\b|\\adventure\\b', '$options': 'i'}}]}
projection: {'title': 1}
count: 324
---
query: {'$or': [{'title': {'$regex': 'western|action|adventure', '$options': 'i'}}, {'plot': {'$regex': 'western|action|adventure', '$options': 'i'}}, {'genres': {'$regex': 'western|action|adventure', '$options': 'i'}}]}
projection: {'title': 1}
count: 452
---
query: {'$text': {'$search': 'western action adventure'}}
projection: {'title': 1}
count: 444
---
query: {'$text': {'$search': 'western action adventure'}}
projection: {'score': {'$meta': 'textScore'}, 'title': 1}
count: 444
```

## References
<https://wiki.apache.org/solr/SolrRelevancyFAQ>
<https://lucene.apache.org/solr/guide/7_6/common-query-parameters.html>
<https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data>
<https://docs.atlas.mongodb.com/import/mongoimport/>
<https://docs.mongodb.com/manual/reference/method/db.collection.find/>
<https://lucidworks.com/2009/09/02/optimizing-findability-in-lucene-and-solr/>
