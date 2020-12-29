# Lyrics Based Recommendation Engine

## Project Description
ML software for hip-hop recommendations from lyrical content without needing user data

## Project Status
- [x] Data scraped
- [x] Run data through ETL (1.prepare for ES ingestion) and (2.make a DF with verse data for machine learning)
- [x] Build and train Gensim Doc2Vec model
- [x] Build and train Sklearn LDA model
- [x] Build Huggingface Transformers NER model
- [x] Add all 3 ML models for extraction and identification as part of ETL process
- [x] Ingest verses and relevant artists into Elasticsearch cluster
- [x] Develop templated ES query to leverage ML models in search with adjustable boosting (surprisingly hard)
- [x] Write Flask API to connect to ES cluster, receive a verse and find similar verses based on embedding, topic extraction, and entity recognition models
- [x] Dockerize Flask API

## Project Tools
- Python
  - Sklearn
  - Gensim
  - Transformers (Huggingface)
  - Flask
  - BS4
  - Json
- Elasticsearch
  - Cosine similarity
  - Custom scoring calculation
  - Adjustable Boosting
- Docker