# Searching with Apache Solr

Materials for the post, [Apache Solr: Because your Database is not a Search Engine](https://wp.me/p1RD28-6e9). In this post, we will examine what sets Apache Solr aside from databases, like MongoDB, as a search engine. We will explore the similarities and differences between Solr and MongoDB by analyzing a series of comparative queries. We then delve into some of Solr’s more advanced search capabilities.

Movie data used in demo publicly available from MongoDB: [Setup and Import the Data](https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data)

## Set-up Instructions

More detailed set-up instructions are in the post, [Apache Solr: Because your Database is not a Search Engine](https://wp.me/p1RD28-6e9).

-   Create MongoDB and Solr Docker containers (commands below)
-   Set (2) environment variables (commands below)
-   Import JSON data to MongoDB (command below)
-   Index JSON data to Solr (command below)
-   Run `query_mongo.py` and `query_solr.py` query scripts

## Useful Commands

Create MongoDB and Solr Docker containers. Solr container bind-mounts config directory from this project.

```bash
docker run --name mongo -p 27017:27017 -d mongo:latest
docker run --name solr -d -p 8983:8983 -v $PWD/conf:/conf solr:latest solr-create -c movies -d /conf

docker logs solr --follow

# docker exec -it --user=solr solr bin/solr create_core -c movies
```

Optional: Copy config from Solr container to local path

```bash
docker run --name solr -p 8983:8983 -d solr:latest solr-create -c movies
docker cp solr:/opt/solr/server/solr/movies/conf/ .
```

Update environment variables with your own values and set

```bash
# local docker example
export SOLR_URL="http://localhost:8983/solr"
export MONOGDB_CONN="mongodb://localhost:27017/movies"

env | grep 'SOLR_URL\|MONOGDB_CONN'
```

Import `movieDetails_mongo.json` JSON data to MongoDB

```bash
mongoimport \
  --uri $MONOGDB_CONN \
  --collection "movieDetails" \
  --drop --file "data/movieDetails_mongo.json"
```

Index JSON data to Solr

```bash
python3 ./solr_index_movies.py
```

FYI Only: Modify Solr movies schema

```bash
curl -X POST \
  "${SOLR_URL}/movies/schema" \
  -H 'Content-Type: application/json' \
  -d '{
  "replace-field":{
     "name":"title",
     "type":"text_en",
     "multiValued":false
  },
  "replace-field":{
     "name":"plot",
     "type":"text_en",
     "multiValued":false
  },
  "replace-field":{
     "name":"genres",
     "type":"text_en",
     "multiValued":true
  }
}'
```

Run query scripts

```bash
time python3 ./query_mongo.py
time python3 ./query_solr.py
```

## Output from Solr Searches

Actually query results are not shown for brevity.

```text
> time python3 ./query_solr.py

----------
Parameters
----------
q: *:*
kwargs: {'defType': 'lucene', 'fl': 'title score', 'sort': 'title asc', 'rows': '5'}

Results
----------
document count: 2250
qtime (ms): 0
----------

Parameters
----------
q: *:*
kwargs: {'defType': 'lucene', 'omitHeader': 'true', 'rows': '0'}

Results
----------
document count: 2250
qtime (ms): None
----------

Parameters
----------
q: "Star Wars: Episode V - The Empire Strikes Back"
kwargs: {'defType': 'lucene', 'df': 'title', 'fl': 'title score'}

Results
----------
document count: 1
qtime (ms): 0
----------

Parameters
----------
q: "star wars"
kwargs: {'defType': 'lucene', 'df': 'title', 'fl': 'title score'}

Results
----------
document count: 6
qtime (ms): 1
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
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 259
qtime (ms): 2
----------

Parameters
----------
q: adventure action western
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title^2.0 genres^4.0', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 259
qtime (ms): 13
----------

Parameters
----------
q: adventure action +western -romance
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title^2.0 genres^4.0', 'fl': 'title genres score', 'rows': '5'}

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
qtime (ms): 0
----------

Parameters
----------
q: The Lego Movie -movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 1
qtime (ms): 11
----------

Parameters
----------
q: A cowboys movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'bq': 'title:movie^-2.0', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 23
qtime (ms): 12
----------

Parameters
----------
q: adventure action +western -romance
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title awards.wins score', 'boost': 'div(field(awards.wins,min),2)', 'rows': '5'}

Results
----------
document count: 25
qtime (ms): 2
----------

Parameters
----------
title: Star Wars: Episode I - The Phantom Menace

Results
----------
id: 7eb78a72-8df8-43c6-9111-b6b45b152b19
----------

Parameters
----------
q: {!mlt qf="genres" mintf=1 mindf=1}7eb78a72-8df8-43c6-9111-b6b45b152b19
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 252
qtime (ms): 20
----------

Parameters
----------
q: id:"7eb78a72-8df8-43c6-9111-b6b45b152b19"
kwargs: {'defType': 'lucene', 'fl': 'actors director writers'}

Results
----------
document count: 1
qtime (ms): 0
----------

Parameters
----------
q: {!mlt qf="actors director writers" mintf=1 mindf=1}7eb78a72-8df8-43c6-9111-b6b45b152b19
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'fl': 'title actors director writers score', 'rows': '10'}

Results
----------
document count: 55
qtime (ms): 2
python3 ./query_solr.py  0.42s user 0.16s system 52% cpu 1.100 total
```

## Output from MongoDB Queries

Actually query results are not shown for brevity.

```text
> time python3 ./query_mongo.py

----------
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
query: {}

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
document count: 18
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
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'genres': 1, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 259
----------

Parameters
----------
query: {'$text': {'$search': 'western action adventure', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'genres': 1, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 259

python3 ./query_mongo.py  0.20s user 0.09s system 17% cpu 1.677 total
```

## References

<https://wiki.apache.org/solr/SolrRelevancyFAQ>
<https://lucene.apache.org/solr/guide/7_6/common-query-parameters.html>
<https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data>
<https://docs.atlas.mongodb.com/import/mongoimport/>
<https://docs.mongodb.com/manual/reference/method/db.collection.find/>
<https://lucidworks.com/2009/09/02/optimizing-findability-in-lucene-and-solr/>
