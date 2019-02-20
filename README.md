# Searching with Apache Solr

Materials for workshop on comparing searching with Apache Solr versus querying in MongoDB: 'Your Database is not a Search Engine'.

Movie data used in demo publicly available from MongoDB: [Setup and Import the Data](https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data)

## Set-up Instructions

Assuming you have an existing MongoDB and Solr instances:

-   Import JSON data to MongoDB (command below)
-   Create Solr `movies` collection (command below)
-   Index JSON data to Solr (Python script: `solr_index_movies.py`)
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
> time python3 ./query_solr.py

Parameters
----------
q: *:*
kwargs: {'defType': 'lucene', 'fl': 'title score', 'sort': 'title asc', 'rows': '5'}

Results
----------
document count: 2250
qtime (ms): 5
----------

Parameters
----------
q: "Star Wars: Episode V - The Empire Strikes Back"
kwargs: {'defType': 'lucene', 'df': 'title', 'fl': 'title score'}

Results
----------
document count: 1
qtime (ms): 2
----------

Parameters
----------
q: "star wars"
kwargs: {'defType': 'lucene', 'df': 'title', 'fl': 'title score'}

Results
----------
document count: 6
qtime (ms): 2
----------

Parameters
----------
q: star wars
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'df': 'title', 'fl': 'title score', 'rows': '5'}

Results
----------
document count: 18
qtime (ms): 1
----------

Parameters
----------
q: (adventure action western)
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'df': 'genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 244
qtime (ms): 1
----------

Parameters
----------
q: (adventure action +western)
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'df': 'genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 24
qtime (ms): 1
----------

Parameters
----------
q: adventure action western
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 259
qtime (ms): 1
----------

Parameters
----------
q: adventure action +western -romance cowboy
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 25
qtime (ms): 2
----------

Parameters
----------
q: A cowboys movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 23
qtime (ms): 1
----------

Parameters
----------
q: The Lego Movie -movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 1
qtime (ms): 2
----------

Parameters
----------
q: A cowboys movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'bq': 'title:movie^-2.0', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 23
qtime (ms): 1
----------

Parameters
----------
title: Star Wars: Episode I - The Phantom Menace

Results
----------
id: 993406a2-cb93-4cd6-bc0b-31b00ea6780f
----------

Parameters
----------
q: {!mlt qf="genres" mintf=1 mindf=1 count }993406a2-cb93-4cd6-bc0b-31b00ea6780f
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 252
qtime (ms): 9
----------

Parameters
----------
q: id:"993406a2-cb93-4cd6-bc0b-31b00ea6780f"
kwargs: {'defType': 'lucene', 'fl': 'actors director writers'}

Results
----------
document count: 1
qtime (ms): 1
----------

Parameters
----------
q: {!mlt qf="actors director writers" mintf=1 mindf=1}993406a2-cb93-4cd6-bc0b-31b00ea6780f
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'fl': 'title actors director writers score', 'rows': '10'}

Results
----------
document count: 82
qtime (ms): 4

python3 ./query_solr.py  0.46s user 0.27s system 32% cpu 2.232 total
```

## Output from MongoDB Queries

Actually documents are not shown for brevity.

```text
> time python3 ./query_mongo.py

Parameters
----------
query: {}
projection: {'_id': 0, 'title': 1}
sort: none

Results
----------
document count: 2250
----------

Parameters
----------
query: {'title': 'Star Wars: Episode V - The Empire Strikes Back'}
projection: {'_id': 0, 'title': 1}
sort: none

Results
----------
document count: 1
----------

Parameters
----------
query: {'title': {'$regex': '\\bstar wars\\b', '$options': 'i'}}
projection: {'_id': 0, 'title': 1}
sort: none

Results
----------
document count: 6
----------

Parameters
----------
query: {'$text': {'$search': 'star wars', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 59
----------

Parameters
----------
query: {'genres': {'$in': ['Adventure', 'Action', 'Western']}, 'countries': 'USA'}
projection: {'_id': 0, 'genres': 1, 'title': 1}
sort: none

Results
----------
document count: 244
----------

Parameters
----------
query: {'$text': {'$search': 'western action adventure', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 259
----------

Parameters
----------
query: {'$text': {'$search': 'Star Wars: Episode V - The Empire Strikes Back', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 103

python3 ./query_mongo.py  0.19s user 0.06s system 15% cpu 1.578 total
```

## References
<https://wiki.apache.org/solr/SolrRelevancyFAQ>
<https://lucene.apache.org/solr/guide/7_6/common-query-parameters.html>
<https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data>
<https://docs.atlas.mongodb.com/import/mongoimport/>
<https://docs.mongodb.com/manual/reference/method/db.collection.find/>
<https://lucidworks.com/2009/09/02/optimizing-findability-in-lucene-and-solr/>
