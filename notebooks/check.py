from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.refresh('production_index')
print(es.cat.count('production_index', params={"format": "json"}))