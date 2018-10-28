import re
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import couchdb
from _datetime import datetime

# get the regex of each kind of symbols
hash_regex = re.compile(r"#(\w+)")
handle_regex = re.compile(r"@(\w+)")
url_regex = re.compile(r"(http|https|ftp://[a-zA-Z0-9\./]+)")
repeat_regex = re.compile(r"(.)\1{1,}(.)\2{1,}", re.IGNORECASE)


# replace hashtags
def hash_replace(matchobj):
    return '__HASH_' + matchobj.group(1).upper()


# replace handles
def handle_replace(matchobj):
    return '_HNDL'


# replace repeat words
def repeat_replace(matchobj):
    res = matchobj.group(1) + matchobj.group(1) + matchobj.group(2)
    return res


# Make an emoticon list
emoticons = \
    [
        (' SMILE ', [':-)', ':)', '(:', '(-:', ';o)', ':o)', ':-3', ':3',
                     ':->', ':>', '8-)', '8)', ':c)', ':^)', '=)']),
        (' LAUGH ', [':-D', ':D', 'X-D', 'x-D', 'XD', 'xD', '=D', '8-D', '8D',
                     '=3', 'B^D', ":'‑)", ":')"]),
        (' LOVE ', ['<3', ':\*']),
        (' GRIN ', [';-)', ';)', ';-D', ';D', '(;', '(-;', '\*-)', '\*)',
                    ';‑]', ';]', ';^)', ':‑,']),
        (' FRUSTRATE ', [':o(', '>:o(', ':-(', ':(', '):', ')-:', ':c', ':‑<',
                         '>:(']),
        (' CRY ', [':,(', ":'(", ':\"(', ':(('])
    ]

# Make an emoji list
emojis = \
    [
        (' SMILE ', ['😁', '😂', '😹', '😃', '😄', '😆', '😊', '😋', '😌', '😍',
                     '😀', '😇', '😛', '😸', '😹', '😺', '😎']),
        (' LAUGH', ['😜', '😝', '😛']),
        (' LOVE ', ['😘', '😚', '😗', '😙', '😻', '😽', '😗', '😙']),
        (' GRIN ', ['😉']),
        (' FRUSTRATE ', ['😔', '😖', '😞', '😠', '😡', '😣', '😨', '😩', '😫',
                         '😰', '😟', '😧']),
        (' CRY ', ['😢', '😭', '😿'])
    ]

# Make a punctuation list
punctuations = \
    [
        ('__PUNC_EXCL', ['!']),
        ('__PUNC_QUES', ['?']),
        ('__PUNC_ELLP', ['...'])
    ]


# remove the parenthesis for emoticon regex and join them together
def rm_parenthesis(arr):
    return [text.replace(')', '[)}\]]').replace('(', '[({\[]') for text in arr]


def res_union(arr):
    return '(' + '|'.join(arr) + ')'


# for emoticon regex
emoticons_regex = [(rep, re.compile(res_union(rm_parenthesis(regex))))
                   for (rep, regex) in emoticons]

# for emoji regex
emojis_regex = [(rep, re.compile(res_union(regex))) for (rep, regex) in emojis]


# substitute or remove all redundant information in a tweet
def process_hashtags(text):
    return re.sub(hash_regex, hash_replace, text)


def process_handles(text):
    return re.sub(handle_regex, handle_replace, text)


def process_urls(text):
    return re.sub(url_regex, '', text)


def process_emoticons(text):
    for (repl, regx) in emoticons_regex:
        text = re.sub(regx, ' ' + repl + ' ', text)
    return text


def process_emojis(text):
    for (repl, regx) in emojis_regex:
        text = re.sub(regx, ' ' + repl + ' ', text)
    return text


def process_repeatings(text):
    return re.sub(repeat_regex, repeat_replace, text)


def process_query_term(text, query):
    query_regex = '|'.join([re.escape(q) for q in query])
    return re.sub(query_regex, '__QUER', text, flags=re.IGNORECASE)


# pre-process the tweet and return the sentiment value
def sentiment_score(analyzer, tweet_text):
    tweet_text = process_urls(tweet_text)
    tweet_text = process_emoticons(tweet_text)
    tweet_text = process_emojis(tweet_text)
    tweet_text = tweet_text.replace('\'', '')
    tweet_text = process_repeatings(tweet_text)
    score = analyzer.polarity_scores(tweet_text)
    return score


# changing a lot
# calculate the properties of a tweet
def sentiment_statistic(analyzer, tweet_text, sentiment_list,db_name):
    score = sentiment_score(analyzer, tweet_text['text'])

    # sentiment_list[db_name]['total'] += score['compound']
    # sentiment_list[db_name]['amount'] += 1
    # if score['compound'] > 0:
    #     sentiment_list[db_name]['positive'] += 1
    # elif score['compound'] < 0:
    #     sentiment_list[db_name]['negative'] += 1
    # else:
    #     sentiment_list[db_name]['neutral'] += 1
    #
    # return sentiment_list
    if  0 <= tweet_text['time'] and tweet_text['time'] <=6 :
        sentiment_list[db_name]['0']['total'] += score['compound']
        sentiment_list[db_name]['0']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['0']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['0']['negative'] += 1
        else:
            sentiment_list[db_name]['0']['neutral'] += 1

    if  tweet_text['time'] == 51 or tweet_text['time'] == 61:
        sentiment_list[db_name]['1']['total'] += score['compound']
        sentiment_list[db_name]['1']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['1']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['1']['negative'] += 1
        else:
            sentiment_list[db_name]['1']['neutral'] += 1



    return sentiment_list

# changing a lot     the meaning of emotion_result
# process each tweet that has been stored in the couchdb, and then update the
# emotion list
def sentiment_analy(analyzer, tweet, emotion_result,db_name):
    emotion_data = emotion_dict()
    emotion_data = sentiment_statistic(analyzer, tweet, emotion_data,db_name)
    # for each city, store the emotion data
    for i in emotion_result:
        emotion_result[i]['0']['total'] += emotion_data[i]['0']['total']
        emotion_result[i]['0']['amount'] += emotion_data[i]['0']['amount']
        emotion_result[i]['0']['positive'] += emotion_data[i]['0']['positive']
        emotion_result[i]['0']['negative'] += emotion_data[i]['0']['negative']
        emotion_result[i]['0']['neutral'] += emotion_data[i]['0']['neutral']
        if emotion_result[i]['0']['amount'] == 0:
            emotion_result[i]['0']['score'] = 'N/A'
        else:
            emotion_result[i]['0']['score'] = emotion_result[i]['0']['total'] / emotion_result[i]['0']['amount']

        emotion_result[i]['1']['total'] += emotion_data[i]['1']['total']
        emotion_result[i]['1']['amount'] += emotion_data[i]['1']['amount']
        emotion_result[i]['1']['positive'] += emotion_data[i]['1']['positive']
        emotion_result[i]['1']['negative'] += emotion_data[i]['1']['negative']
        emotion_result[i]['1']['neutral'] += emotion_data[i]['1']['neutral']
        if emotion_result[i]['1']['amount'] == 0:
            emotion_result[i]['1']['score'] = 'N/A'
        else:
            emotion_result[i]['1']['score'] = emotion_result[i]['1']['total'] / emotion_result[i]['1']['amount']





    return emotion_result


# changing a little bit
# create a dict that records the sentiment scores of different times in one
# day of 8 main cities in Australia
def emotion_dict():
    emotion_score = {
        'bayside-2014': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}

        },
        'bayside-2015': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'bayside-2016': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'bayside-2017': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'bayside-2018': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },

        'dandenong-2014': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'dandenong-2015': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'dandenong-2016': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'dandenong-2017': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'dandenong-2018': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },

        'kingston-2014': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'kingston-2015': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'kingston-2016': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'kingston-2017': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'kingston-2018': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },

        'monash-2014': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'monash-2015': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'monash-2016': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'monash-2017': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'monash-2018': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },

        'stonnington-2014': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'stonnington-2015': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'stonnington-2016': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'stonnington-2017': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'stonnington-2018': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },

        'gleneira-2014': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'gleneira-2015': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'gleneira-2016': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'gleneira-2017': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
        },
        'gleneira-2018': {
            '0': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0}



        }
    }
    return emotion_score


# start process the data and store the result into couchdb
def process_data():
    emotion_result = emotion_dict()
    analyzer = SentimentIntensityAnalyzer()

    couch = couchdb.Server('http://localhost:9000')
    db_list = [
                # 'bayside-2014', 'bayside-2015', 'bayside-2016', 'bayside-2017', 'bayside-2018',
               # 'dandenong-2014', 'dandenong-2015', 'dandenong-2016', 'dandenong-2017', 'dandenong-2018',
               # 'kingston-2014', 'kingston-2015', 'kingston-2016', 'kingston-2017', 'kingston-2018',
               # 'monash-2014', 'monash-2015', 'monash-2016', 'monash-2017', 'monash-2018',
               'stonnington-2014', 'stonnington-2015', 'stonnington-2016', 'stonnington-2017', 'stonnington-2018',
               # 'gleneira-2014', 'gleneira-2015', 'gleneira-2016', 'gleneira-2017', 'gleneira-2018'
    ]

    for db_name in db_list:
        db = couch[db_name]
        print(db_name)
        all_tweets = db.view('_all_docs', include_docs=True)
        for tw in all_tweets:
            to_json = json.dumps(tw['doc'])
            tweet = json.loads(to_json)
            new_tweet = dict()
            new_tweet['text'] = tweet['content']['text']
            # new_tweet['time'] = datetime.strptime(tweet['content']['created_time'],'%a %b %d %H:%M:%S +0000 %Y').hour
            new_tweet['time'] = datetime.strptime(tweet['content']['created_time'],'%a %b %d %H:%M:%S +0000 %Y').weekday()
            emotion_result = sentiment_analy(analyzer, new_tweet, emotion_result,db_name)

    print(emotion_result)
    amount0 = 0
    positive0 = 0
    negative0 = 0
    neutral0 = 0

    amount1 = 0
    positive1 =  0
    negative1 =0
    neutral1 =0



    for k, v in emotion_result.items():
        for m,n in v.items():

            if int(m) == 0:
                amount0 += n['amount']
                positive0 += n['positive']
                negative0 += n['negative']
                neutral0 += n['neutral']

            if int(m) == 1:
                amount1 += n['amount']
                positive1 += n['positive']
                negative1 += n['negative']
                neutral1 += n['neutral']




    print("Weekdays: " + str(amount0) + " positive0 " + str(positive0) + " negative0 " + str(negative0) + " neutral0 " + str(neutral0))
    print("Weekends: " + str(amount1) + " positive1 " + str(positive1) + " negative1 " + str(negative1) + " neutral1 " + str(neutral1))

    # write the result to a new data file in couchdb
    # couch.create('Month')
    # res_db = couch['Month']
    #
    # for city in emotion_result:
    #   city_json = dict()
    #   city_json[city] = emotion_result[city]
    #   res_db.save(city_json)

process_data()
