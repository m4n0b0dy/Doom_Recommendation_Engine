import sys

sys.path.insert(0, '../tools/')
from rap_etl import *

sys.path.insert(0, '../configs/')
from es_config import *

from os.path import isfile, join
from os import listdir
from elasticsearch import Elasticsearch

def validate_index(es_conn, index, body, overwrite = False):
    #check if exists
    if es_conn.indices.exists(index=index) and not overwrite:
        return index, 'already exists'
    #delete current index
    es_conn.indices.delete(index=index,
                      ignore=[400, 404])
    #make index
    return es_conn.indices.create(index=index,
                      ignore=400,
                     body=body)
    
if __name__ == '__main__':
    #connect to ES instance
    es_conn = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    #check if index exists, create if not
    print(validate_index(es_conn,
                         index=ES_INDEX_NAME,
                         body=INDEX_BODY,
                        overwrite=True))
    
    data_repo = '../data/json_lyrics/'
    json_files = [data_repo+f for f in listdir(data_repo) if isfile(join(data_repo, f))]
    json_files = json_files[:10]
    
    #when ingesting with ml pre-processing, doesn't like multiple threads calling a single HF tokenizer model
    #ingest_multiple_json(json_files, es_conn, ES_INDEX_NAME)
    ingest_waterfall_json(json_files, es_conn, ES_INDEX_NAME)