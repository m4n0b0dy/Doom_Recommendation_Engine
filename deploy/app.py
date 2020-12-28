from flask import Flask
from flask import jsonify, request
import sys
sys.path.insert(0, '../configs/')
import es_config

sys.path.insert(0, '../tools/')
from live_models import *


from elasticsearch import Elasticsearch
ES_CONN = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def form_query(embedding,
			   topics,
			   entities,
			   topics_boost=1,
			   entities_boost=1,
			  embedding_boost=1):
	query = {
   "query":{
	  "script_score":{
		 "query":{
			"bool":{
			   "should":[
				  {
					 "match":{
						"verse_topics":{
						   "query":topics,
						   "boost":topics_boost
						}
					 }
				  },
				  {
					 "match":{
						"verse_entities":{
						   "query":' '.join(entities),
						   "boost":entities_boost
						}
					 }
				  }
			   ]
			}
		 },
		 "script":{
			"source":"params.embedding_boost*(cosineSimilarity(params.query_vector, 'verse_vector') + 1.0) + _score",
			"params":{
			   "query_vector":embedding,
			   "embedding_boost":embedding_boost
			}
		 }
	  }
   }
}
	return query

def pull_relevant(results):
	ret_results = []
	for result in results:
		ind_results = {'score':result['_score'],
		'parent_artist':result['_source']['parent_artist'],
		'artist':result['_source']['artist'],
		'album':result['_source']['album'],
		'song':result['_source']['song'],
		'verse_topics':result['_source']['verse_topics'],
		'verse_entities':result['_source']['verse_entities'],
		'verse':result['_source']['verse']}
		ret_results.append(ind_results)
	return ret_results

def run_query(query,size=100):
	results = ES_CONN.search(index=es_config.ES_INDEX_NAME,
		body=query,
		size=size)
	return pull_relevant(results['hits']['hits'])

app = Flask(__name__)
@app.route('/', methods=['GET'])
def verse_es_query():
	payload = request.get_json(force=True)
	verse = payload['verse']
	search_vector = run_embedding(verse)
	search_topics = run_lda(verse)
	search_ents = run_ner(verse)

	topics_boost = payload.get('topics_weight',1)
	entities_boost = payload.get('entities_weight',1)
	embedding_boost = payload.get('verse_weight',1)
	

	query = form_query(embedding=search_vector,
		topics=search_topics,
		entities=search_ents,
		topics_boost=topics_boost,
		entities_boost=entities_boost,
		embedding_boost=embedding_boost)

	results_size = payload.get('query_size',10)

	results = run_query(query,
		size=results_size)
	response = {'query_verse':verse,
				'query_topics':search_topics,
				'query_entities':search_ents,
				'results':results}
	return response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)