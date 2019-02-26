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
```

_Optional: Copy config from Solr container to local path_

```bash
docker run --name solr -p 8983:8983 -d solr:latest solr-create -c movies
docker cp solr:/opt/solr/server/solr/movies/conf/ .
```

_Optional: Create your own core in Solr container_

```bash
docker exec -it --user=solr solr bin/solr create_core -c movies
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

```text
> time python3 ./query_solr.py

Target Solr instance: http://localhost:8983/solr
----------

Parameters
----------
q: *:*
kwargs: {'defType': 'lucene', 'fl': 'title score', 'sort': 'title asc', 'rows': '5'}

Results
----------
document count: 2250
qtime (ms): 2
{'title': 'If....', 'score': 1.0}
{'title': 'To Be or Not to Be', 'score': 1.0}
{'title': 'MW: Dai 0 shô akuma no gêmu', 'score': 1.0}
{'title': 'Km. 0 - Kilometer Zero', 'score': 1.0}
{'title': '0,60 mg', 'score': 1.0}
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
q: title: "Star Wars: Episode V - The Empire Strikes Back"
kwargs: {'defType': 'lucene', 'fl': 'title score'}

Results
----------
document count: 1
qtime (ms): 0
{'title': 'Star Wars: Episode V - The Empire Strikes Back', 'score': 30.66}
----------

Parameters
----------
q: "star wars"
kwargs: {'defType': 'lucene', 'df': 'title', 'fl': 'title score'}

Results
----------
document count: 6
qtime (ms): 0
{'title': 'Star Wars: Episode IV - A New Hope', 'score': 8.27}
{'title': 'Star Wars: Episode VI - Return of the Jedi', 'score': 8.27}
{'title': 'Star Wars: Episode I - The Phantom Menace', 'score': 8.27}
{'title': 'Star Wars: Episode III - Revenge of the Sith', 'score': 8.27}
{'title': 'Star Wars: Episode II - Attack of the Clones', 'score': 8.27}
{'title': 'Star Wars: Episode V - The Empire Strikes Back', 'score': 7.6}
----------

Parameters
----------
q: star wars
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'df': 'title', 'fl': 'title score', 'rows': '5'}

Results
----------
document count: 18
qtime (ms): 0
{'title': 'Star Wars: Episode IV - A New Hope', 'score': 8.27}
{'title': 'Star Wars: Episode VI - Return of the Jedi', 'score': 8.27}
{'title': 'Star Wars: Episode I - The Phantom Menace', 'score': 8.27}
{'title': 'Star Wars: Episode III - Revenge of the Sith', 'score': 8.27}
{'title': 'Star Wars: Episode II - Attack of the Clones', 'score': 8.27}
----------

Parameters
----------
q: adventure action western
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'df': 'genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 244
qtime (ms): 1
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 7.18}
{'title': 'Crossfire Trail', 'genres': ['Action', 'Western'], 'score': 6.26}
{'title': 'The Big Trail', 'genres': ['Adventure', 'Western', 'Romance'], 'score': 5.46}
{'title': 'Once Upon a Time in the West', 'genres': ['Western'], 'score': 5.26}
{'title': 'How the West Was Won', 'genres': ['Western'], 'score': 5.26}
----------

Parameters
----------
q: adventure action +western
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'df': 'genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 24
qtime (ms): 1
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 7.18}
{'title': 'Crossfire Trail', 'genres': ['Action', 'Western'], 'score': 6.26}
{'title': 'The Big Trail', 'genres': ['Adventure', 'Western', 'Romance'], 'score': 5.46}
{'title': 'Once Upon a Time in the West', 'genres': ['Western'], 'score': 5.26}
{'title': 'How the West Was Won', 'genres': ['Western'], 'score': 5.26}
----------

Parameters
----------
q: adventure action western
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 259
qtime (ms): 1
{'title': 'The Secret Life of Walter Mitty', 'genres': ['Adventure', 'Comedy', 'Drama'], 'score': 7.67}
{'title': 'Western Union', 'genres': ['History', 'Western'], 'score': 7.39}
{'title': 'The Adventures of Tintin', 'genres': ['Animation', 'Action', 'Adventure'], 'score': 7.36}
{'title': 'Adventures in Babysitting', 'genres': ['Action', 'Adventure', 'Comedy'], 'score': 7.36}
{'title': 'The Poseidon Adventure', 'genres': ['Action', 'Adventure', 'Drama'], 'score': 7.36}
----------

Parameters
----------
q: adventure action western
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title^2.0 genres^4.0', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 259
qtime (ms): 3
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 28.71}
{'title': 'Crossfire Trail', 'genres': ['Action', 'Western'], 'score': 25.05}
{'title': 'The Big Trail', 'genres': ['Adventure', 'Western', 'Romance'], 'score': 21.84}
{'title': 'Once Upon a Time in the West', 'genres': ['Western'], 'score': 21.05}
{'title': 'How the West Was Won', 'genres': ['Western'], 'score': 21.05}
----------

Parameters
----------
q: adventure action +western -romance
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title^2.0 genres^4.0', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 25
qtime (ms): 4
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 28.71}
{'title': 'Crossfire Trail', 'genres': ['Action', 'Western'], 'score': 25.05}
{'title': 'Once Upon a Time in the West', 'genres': ['Western'], 'score': 21.05}
{'title': 'How the West Was Won', 'genres': ['Western'], 'score': 21.05}
{'title': 'Cowboy', 'genres': ['Western'], 'score': 21.05}
----------

Parameters
----------
q: adventure action +western -romance
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 25
qtime (ms): 1
{'title': 'Western Union', 'genres': ['History', 'Western'], 'score': 7.39}
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 7.18}
{'title': 'Western Spaghetti', 'genres': ['Short'], 'score': 6.64}
{'title': 'Crossfire Trail', 'genres': ['Action', 'Western'], 'score': 6.26}
{'title': 'Butch Cassidy and the Sundance Kid', 'genres': ['Biography', 'Crime', 'Drama'], 'score': 6.23}
----------

Parameters
----------
q: A cowboys movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 23
qtime (ms): 7
{'title': 'Cowboy Bebop: The Movie', 'genres': ['Animation', 'Action', 'Crime'], 'score': 11.24}
{'title': 'Cowboy', 'genres': ['Western'], 'score': 7.31}
{'title': 'TV: The Movie', 'genres': ['Comedy'], 'score': 6.42}
{'title': 'Space Cowboys', 'genres': ['Action', 'Adventure', 'Thriller'], 'score': 6.33}
{'title': 'Midnight Cowboy', 'genres': ['Drama'], 'score': 6.33}
{'title': 'Drugstore Cowboy', 'genres': ['Crime', 'Drama'], 'score': 6.33}
{'title': 'Urban Cowboy', 'genres': ['Drama', 'Romance', 'Western'], 'score': 6.33}
{'title': 'The Cowboy Way', 'genres': ['Action', 'Comedy', 'Drama'], 'score': 6.33}
{'title': 'The Cowboy and the Lady', 'genres': ['Comedy', 'Drama', 'Romance'], 'score': 6.33}
{'title': 'Toy Story', 'genres': ['Animation', 'Adventure', 'Comedy'], 'score': 5.65}
----------

Parameters
----------
q: The Lego Movie -movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 1
qtime (ms): 1
{'title': 'Lego DC Comics Super Heroes: Justice League vs. Bizarro League', 'genres': ['Animation', 'Action', 'Adventure'], 'score': 4.05}
----------

Parameters
----------
q: A cowboys movie
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'bq': 'title:movie^-2.0', 'fl': 'title genres score', 'rows': '10'}

Results
----------
document count: 23
qtime (ms): 1
{'title': 'Cowboy', 'genres': ['Western'], 'score': 7.31}
{'title': 'Space Cowboys', 'genres': ['Action', 'Adventure', 'Thriller'], 'score': 6.33}
{'title': 'Midnight Cowboy', 'genres': ['Drama'], 'score': 6.33}
{'title': 'Drugstore Cowboy', 'genres': ['Crime', 'Drama'], 'score': 6.33}
{'title': 'Urban Cowboy', 'genres': ['Drama', 'Romance', 'Western'], 'score': 6.33}
{'title': 'The Cowboy Way', 'genres': ['Action', 'Comedy', 'Drama'], 'score': 6.33}
{'title': 'The Cowboy and the Lady', 'genres': ['Comedy', 'Drama', 'Romance'], 'score': 6.33}
{'title': 'Toy Story', 'genres': ['Animation', 'Adventure', 'Comedy'], 'score': 5.65}
{'title': "Ride 'Em Cowboy", 'genres': ['Comedy', 'Western', 'Musical'], 'score': 5.58}
{'title': "G.M. Whiting's Enemy", 'genres': ['Mystery'], 'score': 5.32}
----------

Parameters
----------
q: adventure action +western -romance
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title awards.wins score', 'rows': '5'}

Results
----------
document count: 25
qtime (ms): 7
{'title': 'Western Union', 'awards.wins': [0.0], 'score': 7.39}
{'title': 'The Wild Bunch', 'awards.wins': [5.0], 'score': 7.18}
{'title': 'Western Spaghetti', 'awards.wins': [2.0], 'score': 6.64}
{'title': 'Crossfire Trail', 'awards.wins': [1.0], 'score': 6.26}
{'title': 'Butch Cassidy and the Sundance Kid', 'awards.wins': [16.0], 'score': 6.23}
----------

Parameters
----------
q: adventure action +western -romance
kwargs: {'defType': 'edismax', 'fq': 'countries: USA', 'qf': 'plot title genres', 'fl': 'title awards.wins score', 'boost': 'div(field(awards.wins,min),2)', 'rows': '5'}

Results
----------
document count: 25
qtime (ms): 2
{'title': 'Butch Cassidy and the Sundance Kid', 'awards.wins': [16.0], 'score': 49.86}
{'title': 'Wild Wild West', 'awards.wins': [10.0], 'score': 26.03}
{'title': 'How the West Was Won', 'awards.wins': [7.0], 'score': 18.42}
{'title': 'The Wild Bunch', 'awards.wins': [5.0], 'score': 17.95}
{'title': 'All Quiet on the Western Front', 'awards.wins': [5.0], 'score': 13.08}
----------

Parameters
----------
title: Star Wars: Episode I - The Phantom Menace

Results
----------
id: 5b107bec1d2952d0da9046ed
----------

Parameters
----------
q: {!mlt qf="genres" mintf=1 mindf=1}5b107bec1d2952d0da9046ed
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'fl': 'title genres score', 'rows': '5'}

Results
----------
document count: 252
qtime (ms): 1
{'title': 'Star Wars: Episode IV - A New Hope', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 6.33}
{'title': 'Star Wars: Episode V - The Empire Strikes Back', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 6.33}
{'title': 'Star Wars: Episode VI - Return of the Jedi', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 6.33}
{'title': 'Star Wars: Episode III - Revenge of the Sith', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 6.33}
{'title': 'Star Wars: Episode II - Attack of the Clones', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 6.33}
----------

Parameters
----------
q: id:"5b107bec1d2952d0da9046ed"
kwargs: {'defType': 'lucene', 'fl': 'actors director writers'}

Results
----------
document count: 1
qtime (ms): 0
{'director': ['George Lucas'], 'writers': ['George Lucas'], 'actors': ['Liam Neeson', 'Ewan McGregor', 'Natalie Portman', 'Jake Lloyd']}
----------

Parameters
----------
q: {!mlt qf="actors director writers" mintf=1 mindf=1}5b107bec1d2952d0da9046ed
kwargs: {'defType': 'lucene', 'fq': 'countries: USA', 'fl': 'title actors director writers score', 'rows': '10'}

Results
----------
document count: 55
qtime (ms): 1
{'title': 'Star Wars: Episode III - Revenge of the Sith', 'director': ['George Lucas'], 'writers': ['George Lucas'], 'actors': ['Ewan McGregor', 'Natalie Portman', 'Hayden Christensen', 'Ian McDiarmid'], 'score': 44.84}
{'title': 'Star Wars: Episode II - Attack of the Clones', 'director': ['George Lucas'], 'writers': ['George Lucas', 'Jonathan Hales', 'George Lucas'], 'actors': ['Ewan McGregor', 'Natalie Portman', 'Hayden Christensen', 'Christopher Lee'], 'score': 44.58}
{'title': 'Star Wars: Episode IV - A New Hope', 'director': ['George Lucas'], 'writers': ['George Lucas'], 'actors': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher', 'Peter Cushing'], 'score': 23.51}
{'title': 'Star Wars: Episode VI - Return of the Jedi', 'director': ['Richard Marquand'], 'writers': ['Lawrence Kasdan', 'George Lucas', 'George Lucas'], 'actors': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher', 'Billy Dee Williams'], 'score': 11.96}
{'title': 'A Million Ways to Die in the West', 'director': ['Seth MacFarlane'], 'writers': ['Seth MacFarlane', 'Alec Sulkin', 'Wellesley Wild'], 'actors': ['Seth MacFarlane', 'Charlize Theron', 'Amanda Seyfried', 'Liam Neeson'], 'score': 11.72}
{'title': 'Run All Night', 'director': ['Jaume Collet-Serra'], 'writers': ['Brad Ingelsby'], 'actors': ['Liam Neeson', 'Ed Harris', 'Joel Kinnaman', 'Boyd Holbrook'], 'score': 11.72}
{'title': 'I Love You Phillip Morris', 'director': ['Glenn Ficarra, John Requa'], 'writers': ['John Requa', 'Glenn Ficarra', 'Steve McVicker'], 'actors': ['Jim Carrey', 'Ewan McGregor', 'Leslie Mann', 'Rodrigo Santoro'], 'score': 10.97}
{'title': 'The Island', 'director': ['Michael Bay'], 'writers': ['Caspian Tredwell-Owen', 'Alex Kurtzman', 'Roberto Orci', 'Caspian Tredwell-Owen'], 'actors': ['Ewan McGregor', 'Scarlett Johansson', 'Djimon Hounsou', 'Sean Bean'], 'score': 10.97}
{'title': 'Big Fish', 'director': ['Tim Burton'], 'writers': ['Daniel Wallace', 'John August'], 'actors': ['Ewan McGregor', 'Albert Finney', 'Billy Crudup', 'Jessica Lange'], 'score': 10.97}
{'title': 'New Meet Me on South Street: The Story of JC Dobbs', 'director': ['George Manney'], 'writers': ['George Manney'], 'actors': ['Tony Bidgood', 'Peter Stone Brown', 'Stephen Caldwell', 'Tommy Conwell'], 'score': 10.5}
----------

Parameters
----------
q: ciborg
kwargs: {'defType': 'edismax', 'qf': 'title plot genres', 'fl': 'title score', 'stopwords': 'true', 'rows': '5'}

Results
----------
document count: 2
qtime (ms): 0
{'title': 'Terminator 2: Judgment Day', 'score': 8.17}
{'title': "I'm a Cyborg, But That's OK", 'score': 7.13}
----------

Parameters
----------
q: droid
kwargs: {'defType': 'edismax', 'qf': 'title plot genres', 'fl': 'title score', 'stopwords': 'true', 'rows': '5'}

Results
----------
document count: 15
qtime (ms): 2
{'title': 'Robo Jî', 'score': 7.67}
{'title': "I'm a Cyborg, But That's OK", 'score': 7.13}
{'title': 'BV-01', 'score': 6.6}
{'title': 'Robot Chicken: DC Comics Special', 'score': 6.44}
{'title': 'Terminator 2: Judgment Day', 'score': 6.23}
----------

Parameters
----------
q: scary
kwargs: {'defType': 'edismax', 'qf': 'title plot genres', 'fl': 'title score', 'stopwords': 'true', 'rows': '5'}

Results
----------
document count: 141
qtime (ms): 0
{'title': 'See No Evil, Hear No Evil', 'score': 7.9}
{'title': 'The Evil Dead', 'score': 7.23}
{'title': 'Evil Dead', 'score': 7.23}
{'title': 'Evil Ed', 'score': 7.23}
{'title': 'Evil Dead II', 'score': 6.37}
----------

Parameters
----------
q: lol
kwargs: {'defType': 'edismax', 'qf': 'title plot genres', 'fl': 'title score', 'stopwords': 'true', 'rows': '5'}

Results
----------
document count: 1
qtime (ms): 2
{'title': 'JK LOL', 'score': 9.05}

python3 ./query_solr.py  0.47s user 0.20s system 42% cpu 1.559 total
```

## Output from MongoDB Queries

```text
> time python3 ./query_mongo.py

Target MongoDB instance: mongodb://localhost:27017/movies
No index to remove
----------

Parameters
----------
query: {}
projection: {'_id': 0, 'title': 1}
sort: none

Results
----------
document count: 2250
{'title': 'West Side Story'}
{'title': 'A Million Ways to Die in the West'}
{'title': 'Once Upon a Time in the West'}
{'title': 'Wild Wild West'}
{'title': 'An American Tail: Fievel Goes West'}
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
{'title': 'Star Wars: Episode V - The Empire Strikes Back'}
----------

Parameters
----------
query: {'title': {'$regex': '\\bstar wars\\b', '$options': 'i'}}
projection: {'_id': 0, 'title': 1}
sort: none

Results
----------
document count: 6
{'title': 'Star Wars: Episode I - The Phantom Menace'}
{'title': 'Star Wars: Episode II - Attack of the Clones'}
{'title': 'Star Wars: Episode III - Revenge of the Sith'}
{'title': 'Star Wars: Episode IV - A New Hope'}
{'title': 'Star Wars: Episode V - The Empire Strikes Back'}
----------

Parameters
----------
query: {'$text': {'$search': 'star wars', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 18
{'title': 'Star Wars: Episode I - The Phantom Menace', 'score': 1.2}
{'title': 'Star Wars: Episode IV - A New Hope', 'score': 1.17}
{'title': 'Star Wars: Episode III - Revenge of the Sith', 'score': 1.17}
{'title': 'Star Wars: Episode VI - Return of the Jedi', 'score': 1.17}
{'title': 'Star Wars: Episode II - Attack of the Clones', 'score': 1.17}
----------

Parameters
----------
query: {'genres': {'$in': ['Adventure', 'Action', 'Western']}, 'countries': 'USA'}
projection: {'_id': 0, 'genres': 1, 'title': 1}
sort: none

Results
----------
document count: 244
{'title': 'A Million Ways to Die in the West', 'genres': ['Comedy', 'Western']}
{'title': 'Once Upon a Time in the West', 'genres': ['Western']}
{'title': 'Wild Wild West', 'genres': ['Action', 'Western', 'Comedy']}
{'title': 'An American Tail: Fievel Goes West', 'genres': ['Animation', 'Adventure', 'Family']}
{'title': 'How the West Was Won', 'genres': ['Western']}
----------

Parameters
----------
query: {'$text': {'$search': 'western action adventure', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'genres': 1, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 259
{'title': 'Zathura: A Space Adventure', 'genres': ['Action', 'Adventure', 'Comedy'], 'score': 3.3}
{'title': 'The Extraordinary Adventures of Adèle Blanc-Sec', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 3.24}
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 3.2}
{'title': 'The Adventures of Tintin', 'genres': ['Animation', 'Action', 'Adventure'], 'score': 2.85}
{'title': 'Adventures in Babysitting', 'genres': ['Action', 'Adventure', 'Comedy'], 'score': 2.85}
----------

Parameters
----------
query: {'$text': {'$search': 'western action adventure', '$language': 'en', '$caseSensitive': False}, 'countries': 'USA'}
projection: {'score': {'$meta': 'textScore'}, '_id': 0, 'genres': 1, 'title': 1}
sort: [('score', {'$meta': 'textScore'})]

Results
----------
document count: 259
{'title': 'The Wild Bunch', 'genres': ['Action', 'Adventure', 'Western'], 'score': 12.8}
{'title': 'Zathura: A Space Adventure', 'genres': ['Action', 'Adventure', 'Comedy'], 'score': 10.27}
{'title': 'The Extraordinary Adventures of Adèle Blanc-Sec', 'genres': ['Action', 'Adventure', 'Fantasy'], 'score': 10.14}
{'title': 'The Adventures of Tintin', 'genres': ['Animation', 'Action', 'Adventure'], 'score': 9.9}
{'title': 'Adventures in Babysitting', 'genres': ['Action', 'Adventure', 'Comedy'], 'score': 9.9}

python3 ./query_mongo.py  0.21s user 0.11s system 18% cpu 1.716 total
```

## References

<https://wiki.apache.org/solr/SolrRelevancyFAQ>
<https://lucene.apache.org/solr/guide/7_6/common-query-parameters.html>
<https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data>
<https://docs.atlas.mongodb.com/import/mongoimport/>
<https://docs.mongodb.com/manual/reference/method/db.collection.find/>
<https://lucidworks.com/2009/09/02/optimizing-findability-in-lucene-and-solr/>
