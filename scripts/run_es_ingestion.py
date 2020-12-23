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
    #leaving out as I really dont need this for now
    '''print(validate_index(es_conn,
                                     index=ES_INDEX_NAME,
                                     body=INDEX_BODY,
                                    overwrite=False))
                '''
    data_repo = '../data/json_lyrics/'
    json_files = [data_repo+f for f in listdir(data_repo) if isfile(join(data_repo, f))]
    with open('success.txt') as f:
      done = f.read().split(', ')
    filtered_json_files = [_ for _ in json_files if _ not in done]
    print('All Files:',len(json_files))
    print('Completed:', len(done))
    print('Left to go:',len(filtered_json_files))
    #when ingesting with ml pre-processing, doesn't like multiple threads calling a single HF tokenizer model
    #ingest_multiple_json(filtered_json_files, es_conn, ES_INDEX_NAME)
    ingest_waterfall_json(filtered_json_files, es_conn, ES_INDEX_NAME)
