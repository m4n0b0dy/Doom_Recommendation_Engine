import json
import re
from itertools import repeat
import time

from live_models import *

import sys
sys.path.insert(0, '../configs/')
from es_config import *

from multiprocessing.pool import ThreadPool as Pool
thread_count = 10

class Verse:
    def __init__(self,
                 raw_text,
                 parent_artist=None,
                 artist=None,
                 album=None,
                 song=None):
        self.text = raw_text
        self.es_dict = {
            'parent_artist':parent_artist,
            'artist':artist,
            'album':album,
            'song':song,
            'verse':self.text,
            'verse_vector':[],
            'verse_topics':'',
            'verse_entities':[],
        }
        
    def clean_text(self):
        _text = self.text
        for pattern, replacement in REGEX_PATTERNS.items():
            _text = re.sub(pattern, replacement, _text)
        self.text = _text.strip()
        self.es_dict['verse'] = self.text
    
    #not really best practice here but was simpler than the other method
    def run_all_ml_models(self):
        self.es_dict['verse_vector'] = run_embedding(self.text)
        self.es_dict['verse_topics'] = run_lda(self.text)
        self.es_dict['verse_entities'] = run_ner(self.text)
        

    def ingest_to_es(self,conn,index):
        return conn.index(index=index, body=self.es_dict)
    
    
def load_artist_es(json_path, es_conn, es_index):
    t = time.time()
    with open(json_path) as f:
        data = json.load(f)
    parent_artist = json_path.replace('.json','').replace('../data/json_lyrics/','')
    cntr = 0
    for artist, albums in data.items():
        if 'raw_song_' in artist:
            text = albums
            albums = {'unknown':{'unknown':text}}
        for album, songs in albums.items():
            for song,text in songs.items():
                verse = Verse(raw_text=text,
                            parent_artist=parent_artist,
                            artist=artist,
                            album=album,
                            song=song)
                #clean verse for known bad texts
                verse.clean_text()
                #run ml models and set attributes
                verse.run_all_ml_models()
                #ingest to elastisearch
                verse.ingest_to_es(es_conn,
                               es_index)
                cntr +=1
    print('Ingested',cntr,'songs for json file:',json_path,'in time:',time.time()-t)

#not good to copy code but don't want to overwrite an etl function
def verse_extract(json_path):
    t = time.time()
    with open(json_path) as f:
        data = json.load(f)
    parent_artist = json_path.replace('.json','').replace('../data/json_lyrics/','')
    full_verse_list = []
    for artist, albums in data.items():
        if 'raw_song_' in artist:
            text = albums
            albums = {'unknown':{'unknown':text}}
        for album, songs in albums.items():
            for song,text in songs.items():
                verse = Verse(raw_text=text,
                            parent_artist=parent_artist,
                            artist=artist,
                            album=album,
                            song=song)
                verse.clean_text()
                full_verse_list.append({'parent_artist':parent_artist,
                                       'artist':artist,
                                       'album':album,
                                       'song':song,
                                       'verse':verse.text})
    print('Extracted',json_path,'in time:',time.time()-t)
    return full_verse_list                

def ingest_waterfall_json(json_paths,es_conn,es_index):
    for json_path in json_paths:
        load_artist_es(json_path, es_conn, es_index)

def ingest_multiple_json(json_paths,es_conn,es_index):
    pool = Pool(thread_count)
    pool.starmap(load_artist_es, zip(json_paths, repeat(es_conn), repeat(es_index)))
    pool.close()
    pool.join()