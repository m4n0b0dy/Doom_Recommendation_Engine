import json
import re
from itertools import repeat
import time

import sys
sys.path.insert(0, '../configs/')
from es_config import *

from multiprocessing.pool import ThreadPool as Pool
thread_count = 500

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
            'raw_verse':self.text,
            'verse_vector':[0,0]
        }
        
    def clean_text(self):
        _text = self.text
        for pattern, replacement in REGEX_PATTERNS.items():
            _text = re.sub(pattern, replacement, _text)
        self.text = _text.strip()
        self.es_dict['verse'] = self.text

    def ingest_to_es(self,conn,index):
        return conn.index(index=index, body=self.es_dict)
    
def etl_artist(json_path, es_conn, es_index):
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
                verse.clean_text()
                verse.ingest_to_es(es_conn,
                               es_index)
                cntr +=1
    print('Ingested',cntr,'songs for json file:',json_path,'in time:',time.time()-t)

def ingest_multiple_json(json_paths,es_conn,es_index):
    pool = Pool(thread_count)
    pool.starmap(etl_artist, zip(json_paths, repeat(es_conn), repeat(es_index)))
    pool.close()
    pool.join()