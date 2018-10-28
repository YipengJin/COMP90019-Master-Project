import json
import couchdb
import spacy

spacy.load('en')
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def process_data():
    #emotion_result = emotion_dict()
    #analyzer = SentimentIntensityAnalyzer()

    couch = couchdb.Server('http://localhost:9000')
    db_list = ['poly2014', 'poly2015', 'poly2016', 'poly2017', 'poly2018']

    for db_name in db_list:
        db = couch[db_name]
        all_tweets = db.view('_all_docs', include_docs=True)
        for tw in all_tweets:
            to_json = json.dumps(tw['doc'])
            tweet = json.loads(to_json)
            new_tweet = dict()
            new_tweet['text'] = tweet['content']['text']
            print(tokenize(new_tweet['text']))

process_data()