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
export MONOGDB_CONN="mongodb+srv://{{ user }}:{{ password }}@{{ host }}/admin"
```

Import `movieDetails_mongo.json` JSON data to MongoDB

```bash
mongoimport \
  --uri $MONOGDB_CONN \
  --collection "movieDetails" \
  --drop --file "data/movieDetails_mongo.json"
```

## References

<https://lucene.apache.org/solr/guide/7_6/common-query-parameters.html>
<https://docs.mongodb.com/charts/master/tutorial/movie-details/prereqs-and-import-data/#download-the-data>
<https://docs.atlas.mongodb.com/import/mongoimport/>
