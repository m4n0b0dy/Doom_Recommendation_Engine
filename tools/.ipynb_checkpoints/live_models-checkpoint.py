from gensim.parsing.porter import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
import _pickle as cPickle
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
#python file to laod in all my models all at once
#not using main because these are variables across files

#stemmer for embeddings
STEMMER = PorterStemmer()
def stem_and_stop(verse):
    verse = remove_stopwords(verse)
    if not verse:
        return ['']
    verse = STEMMER.stem_sentence(verse)
    return simple_preprocess(verse)

#embedding model
EMBEDDING_MODEL = Doc2Vec.load("../models/doc2vec/doc2vec.model")

def run_embedding(string):
    word_list = stem_and_stop(string)
    return EMBEDDING_MODEL.infer_vector(word_list)

#lda model
#load lda model
with open('../models/lda/lda.pkl', 'rb') as f:
    LDA_MODEL = cPickle.load(f)
#load the vectorizer
with open('../models/lda/vectorizer.pkl', 'rb') as f:
    COUNT_VECTORIZER = cPickle.load(f)
#Simple function to get topics out of model, need to do once
def get_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    topic_lists = []
    for topic_idx, topic in enumerate(model.components_):
        topic_list = [words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topic_lists.append(topic_list)
    return topic_lists
ALL_TOPICS = get_topics(LDA_MODEL,COUNT_VECTORIZER, 10)#10 is what it was trained on

#join topics to each topic's probability
def run_lda(string, topic_threshold=.5):
    vectorized = COUNT_VECTORIZER.transform([string])
    pred = LDA_MODEL.transform(vectorized)
    topics = sorted(list(zip(pred[0],ALL_TOPICS)),reverse=True)
    if topics[0][0]>=topic_threshold:
        return ' + '.join(topics[0][1])
    else:
        return ''

#NER model
tokenizer = AutoTokenizer.from_pretrained("../models/bert_ner/tokenizer/")
model = AutoModelForTokenClassification.from_pretrained("../models/bert_ner/model/")
NER_MODEL = pipeline("ner", model=model, tokenizer=tokenizer)

def run_ner(string):
    ner_results = NER_MODEL(string)
    return [_['word'] for _ in ner_results]