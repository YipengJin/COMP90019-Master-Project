from spacy.lang.en import English
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora
import pickle
import gensim
import pyLDAvis.gensim
import json
import couchdb
import spacy
import nltk

nltk.download('wordnet')
spacy.load('en')
parser = English()
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))
text_data = []

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return ' '.join(tokens)

def process_data():
    couch = couchdb.Server('http://localhost:9000')
    db_list = ['gleneira-2014', 'gleneira-2015', 'gleneira-2016', 'gleneira-2017', 'gleneira-2018']

    for db_name in db_list:
        db = couch[db_name]
        all_tweets = db.view('_all_docs', include_docs=True)
        for tw in all_tweets:
            to_json = json.dumps(tw['doc'])
            tweet = json.loads(to_json)
            new_tweet = dict()
            new_tweet['text'] = tweet['content']['text']
            # print(prepare_text_for_lda(new_tweet['text']))
            text_data.append(prepare_text_for_lda(new_tweet['text']))
    return text_data

process_data()

print process_data()
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
n_features = 1000

tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df = 0.5,
                                min_df = 10)
tf = tf_vectorizer.fit_transform(process_data())

from sklearn.decomposition import LatentDirichletAllocation

n_topics = 5
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

lda.fit(tf)

LatentDirichletAllocation(batch_size=128, doc_topic_prior=None,
             evaluate_every=-1, learning_decay=0.7,
             learning_method='online', learning_offset=50.0,
             max_doc_update_iter=100, max_iter=50, mean_change_tol=0.001,
             n_jobs=1, n_topics=5, perp_tol=0.1, random_state=0,
             topic_word_prior=None, total_samples=1000000.0, verbose=0)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
n_top_words = 3

tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

import pyLDAvis
import pyLDAvis.sklearn
# pyLDAvis.enable_notebook()
# pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.show(data)