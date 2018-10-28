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
    if  tweet_text['time'] == 1:
        sentiment_list[db_name]['1']['total'] += score['compound']
        sentiment_list[db_name]['1']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['1']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['1']['negative'] += 1
        else:
            sentiment_list[db_name]['1']['neutral'] += 1

    elif  tweet_text['time'] == 2:
        sentiment_list[db_name]['2']['total'] += score['compound']
        sentiment_list[db_name]['2']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['2']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['2']['negative'] += 1
        else:
            sentiment_list[db_name]['2']['neutral'] += 1

    elif tweet_text['time'] ==3:
        sentiment_list[db_name]['3']['total'] += score['compound']
        sentiment_list[db_name]['3']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['3']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['3']['negative'] += 1
        else:
            sentiment_list[db_name]['3']['neutral'] += 1

    elif tweet_text['time'] == 4:
        sentiment_list[db_name]['4']['total'] += score['compound']
        sentiment_list[db_name]['4']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['4']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['4']['negative'] += 1
        else:
            sentiment_list[db_name]['4']['neutral'] += 1

    elif tweet_text['time'] == 5:
        sentiment_list[db_name]['5']['total'] += score['compound']
        sentiment_list[db_name]['5']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['5']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['5']['negative'] += 1
        else:
            sentiment_list[db_name]['5']['neutral'] += 1

    elif tweet_text['time'] == 6:
        sentiment_list[db_name]['6']['total'] += score['compound']
        sentiment_list[db_name]['6']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['6']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['6']['negative'] += 1
        else:
            sentiment_list[db_name]['6']['neutral'] += 1

    elif tweet_text['time'] == 7:
        sentiment_list[db_name]['7']['total'] += score['compound']
        sentiment_list[db_name]['7']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['7']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['7']['negative'] += 1
        else:
            sentiment_list[db_name]['7']['neutral'] += 1

    elif tweet_text['time'] == 8:
        sentiment_list[db_name]['8']['total'] += score['compound']
        sentiment_list[db_name]['8']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['8']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['8']['negative'] += 1
        else:
            sentiment_list[db_name]['8']['neutral'] += 1

    elif tweet_text['time'] == 9:
        sentiment_list[db_name]['9']['total'] += score['compound']
        sentiment_list[db_name]['9']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['9']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['9']['negative'] += 1
        else:
            sentiment_list[db_name]['9']['neutral'] += 1

    elif tweet_text['time'] == 10:
        sentiment_list[db_name]['10']['total'] += score['compound']
        sentiment_list[db_name]['10']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['10']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['10']['negative'] += 1
        else:
            sentiment_list[db_name]['10']['neutral'] += 1

    elif tweet_text['time'] == 11:
        sentiment_list[db_name]['11']['total'] += score['compound']
        sentiment_list[db_name]['11']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['11']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['11']['negative'] += 1
        else:
            sentiment_list[db_name]['11']['neutral'] += 1

    elif tweet_text['time'] == 12:
        sentiment_list[db_name]['12']['total'] += score['compound']
        sentiment_list[db_name]['12']['amount'] += 1
        if score['compound'] > 0:
            sentiment_list[db_name]['12']['positive'] += 1
        elif score['compound'] < 0:
            sentiment_list[db_name]['12']['negative'] += 1
        else:
            sentiment_list[db_name]['12']['neutral'] += 1

    return sentiment_list

# changing a lot     the meaning of emotion_result
# process each tweet that has been stored in the couchdb, and then update the
# emotion list
def sentiment_analy(analyzer, tweet, emotion_result,db_name):
    emotion_data = emotion_dict()
    emotion_data = sentiment_statistic(analyzer, tweet, emotion_data,db_name)
    # for each city, store the emotion data
    for i in emotion_result:
        # tweets from 0am to 6am
        emotion_result[i]['1']['total'] += emotion_data[i]['1']['total']
        emotion_result[i]['1']['amount'] += emotion_data[i]['1']['amount']
        emotion_result[i]['1']['positive'] += emotion_data[i]['1']['positive']
        emotion_result[i]['1']['negative'] += emotion_data[i]['1']['negative']
        emotion_result[i]['1']['neutral'] += emotion_data[i]['1']['neutral']
        if emotion_result[i]['1']['amount'] == 0:
            emotion_result[i]['1']['score'] = 'N/A'
        else:
            emotion_result[i]['1']['score'] = emotion_result[i]['1']['total'] / emotion_result[i]['1']['amount']

        # tweets from 6am to 12pm
        emotion_result[i]['2']['total'] += emotion_data[i]['2']['total']
        emotion_result[i]['2']['amount'] += emotion_data[i]['2']['amount']
        emotion_result[i]['2']['positive'] += emotion_data[i]['2']['positive']
        emotion_result[i]['2']['negative'] += emotion_data[i]['2']['negative']
        emotion_result[i]['2']['neutral'] += emotion_data[i]['2']['neutral']
        if emotion_result[i]['2']['amount'] == 0:
            emotion_result[i]['2']['score'] = 'N/A'
        else:
            emotion_result[i]['2']['score'] = emotion_result[i]['2']['total'] / emotion_result[i]['2'][
                'amount']

        # tweets from 12pm to 6pm
        emotion_result[i]['3']['total'] += emotion_data[i]['3']['total']
        emotion_result[i]['3']['amount'] += emotion_data[i]['3']['amount']
        emotion_result[i]['3']['positive'] += emotion_data[i]['3']['positive']
        emotion_result[i]['3']['negative'] += emotion_data[i]['3']['negative']
        emotion_result[i]['3']['neutral'] += emotion_data[i]['3']['neutral']
        if emotion_result[i]['3']['amount'] == 0:
            emotion_result[i]['3']['score'] = 'N/A'
        else:
            emotion_result[i]['3']['score'] = emotion_result[i]['3']['total'] / emotion_result[i]['3'][
                'amount']

        # tweets from 6pm to 12am
        emotion_result[i]['4']['total'] += emotion_data[i]['4']['total']
        emotion_result[i]['4']['amount'] += emotion_data[i]['4']['amount']
        emotion_result[i]['4']['positive'] += emotion_data[i]['4']['positive']
        emotion_result[i]['4']['negative'] += emotion_data[i]['4']['negative']
        emotion_result[i]['4']['neutral'] += emotion_data[i]['4']['neutral']
        if emotion_result[i]['4']['amount'] == 0:
            emotion_result[i]['4']['score'] = 'N/A'
        else:
            emotion_result[i]['4']['score'] = emotion_result[i]['4']['total'] / emotion_result[i]['4'][
                'amount']

        emotion_result[i]['5']['total'] += emotion_data[i]['5']['total']
        emotion_result[i]['5']['amount'] += emotion_data[i]['5']['amount']
        emotion_result[i]['5']['positive'] += emotion_data[i]['5']['positive']
        emotion_result[i]['5']['negative'] += emotion_data[i]['5']['negative']
        emotion_result[i]['5']['neutral'] += emotion_data[i]['5']['neutral']
        if emotion_result[i]['5']['amount'] == 0:
            emotion_result[i]['5']['score'] = 'N/A'
        else:
            emotion_result[i]['5']['score'] = emotion_result[i]['5']['total'] / emotion_result[i]['5'][
                'amount']

        emotion_result[i]['6']['total'] += emotion_data[i]['6']['total']
        emotion_result[i]['6']['amount'] += emotion_data[i]['6']['amount']
        emotion_result[i]['6']['positive'] += emotion_data[i]['6']['positive']
        emotion_result[i]['6']['negative'] += emotion_data[i]['6']['negative']
        emotion_result[i]['6']['neutral'] += emotion_data[i]['6']['neutral']
        if emotion_result[i]['6']['amount'] == 0:
            emotion_result[i]['6']['score'] = 'N/A'
        else:
            emotion_result[i]['6']['score'] = emotion_result[i]['6']['total'] / emotion_result[i]['6'][
                'amount']

        emotion_result[i]['7']['total'] += emotion_data[i]['7']['total']
        emotion_result[i]['7']['amount'] += emotion_data[i]['7']['amount']
        emotion_result[i]['7']['positive'] += emotion_data[i]['7']['positive']
        emotion_result[i]['7']['negative'] += emotion_data[i]['7']['negative']
        emotion_result[i]['7']['neutral'] += emotion_data[i]['7']['neutral']
        if emotion_result[i]['7']['amount'] == 0:
            emotion_result[i]['7']['score'] = 'N/A'
        else:
            emotion_result[i]['7']['score'] = emotion_result[i]['7']['total'] / emotion_result[i]['7'][
                'amount']

        emotion_result[i]['8']['total'] += emotion_data[i]['8']['total']
        emotion_result[i]['8']['amount'] += emotion_data[i]['8']['amount']
        emotion_result[i]['8']['positive'] += emotion_data[i]['8']['positive']
        emotion_result[i]['8']['negative'] += emotion_data[i]['8']['negative']
        emotion_result[i]['8']['neutral'] += emotion_data[i]['8']['neutral']
        if emotion_result[i]['8']['amount'] == 0:
            emotion_result[i]['8']['score'] = 'N/A'
        else:
            emotion_result[i]['8']['score'] = emotion_result[i]['8']['total'] / emotion_result[i]['8'][
                'amount']

        emotion_result[i]['9']['total'] += emotion_data[i]['9']['total']
        emotion_result[i]['9']['amount'] += emotion_data[i]['9']['amount']
        emotion_result[i]['9']['positive'] += emotion_data[i]['9']['positive']
        emotion_result[i]['9']['negative'] += emotion_data[i]['9']['negative']
        emotion_result[i]['9']['neutral'] += emotion_data[i]['9']['neutral']
        if emotion_result[i]['9']['amount'] == 0:
            emotion_result[i]['9']['score'] = 'N/A'
        else:
            emotion_result[i]['9']['score'] = emotion_result[i]['9']['total'] / emotion_result[i]['9'][
                'amount']

        emotion_result[i]['10']['total'] += emotion_data[i]['10']['total']
        emotion_result[i]['10']['amount'] += emotion_data[i]['10']['amount']
        emotion_result[i]['10']['positive'] += emotion_data[i]['10']['positive']
        emotion_result[i]['10']['negative'] += emotion_data[i]['10']['negative']
        emotion_result[i]['10']['neutral'] += emotion_data[i]['10']['neutral']
        if emotion_result[i]['10']['amount'] == 0:
            emotion_result[i]['10']['score'] = 'N/A'
        else:
            emotion_result[i]['10']['score'] = emotion_result[i]['10']['total'] / emotion_result[i]['10'][
                'amount']

        emotion_result[i]['11']['total'] += emotion_data[i]['11']['total']
        emotion_result[i]['11']['amount'] += emotion_data[i]['11']['amount']
        emotion_result[i]['11']['positive'] += emotion_data[i]['11']['positive']
        emotion_result[i]['11']['negative'] += emotion_data[i]['11']['negative']
        emotion_result[i]['11']['neutral'] += emotion_data[i]['11']['neutral']
        if emotion_result[i]['11']['amount'] == 0:
            emotion_result[i]['11']['score'] = 'N/A'
        else:
            emotion_result[i]['11']['score'] = emotion_result[i]['11']['total'] / emotion_result[i]['11'][
                'amount']

        emotion_result[i]['12']['total'] += emotion_data[i]['12']['total']
        emotion_result[i]['12']['amount'] += emotion_data[i]['12']['amount']
        emotion_result[i]['12']['positive'] += emotion_data[i]['12']['positive']
        emotion_result[i]['12']['negative'] += emotion_data[i]['12']['negative']
        emotion_result[i]['12']['neutral'] += emotion_data[i]['12']['neutral']
        if emotion_result[i]['12']['amount'] == 0:
            emotion_result[i]['12']['score'] = 'N/A'
        else:
            emotion_result[i]['12']['score'] = emotion_result[i]['12']['total'] / emotion_result[i]['12'][
                'amount']

    return emotion_result


# changing a little bit
# create a dict that records the sentiment scores of different times in one
# day of 8 main cities in Australia
def emotion_dict():
    emotion_score = {
        'bayside-2014': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'bayside-2015': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'bayside-2016': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'bayside-2017': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'bayside-2018': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },

        'dandenong-2014': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'dandenong-2015': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'dandenong-2016': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'dandenong-2017': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'dandenong-2018': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },

        'kingston-2014': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'kingston-2015': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'kingston-2016': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'kingston-2017': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'kingston-2018': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },

        'monash-2014': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'monash-2015': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'monash-2016': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'monash-2017': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'monash-2018': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },

        'stonnington-2014': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'stonnington-2015': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'stonnington-2016': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'stonnington-2017': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'stonnington-2018': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },

        'gleneira-2014': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'gleneira-2015': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'gleneira-2016': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'gleneira-2017': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
        },
        'gleneira-2018': {
            '1': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '2': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '3': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '4': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '5': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '6': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '7': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '8': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '9': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '10': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '11': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},
            '12': {'total': 0, 'amount': 0, 'positive': 0, 'negative': 0, 'neutral': 0},


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
            new_tweet['time'] = datetime.strptime(tweet['content']['created_time'],'%a %b %d %H:%M:%S +0000 %Y').month
            # print(new_tweet['time'])
            emotion_result = sentiment_analy(analyzer, new_tweet, emotion_result,db_name)

    print(emotion_result)
    amount1 = 0
    positive1 =  0
    negative1 =0
    neutral1 =0

    amount2 = 0
    positive2 = 0
    negative2 = 0
    neutral2 = 0

    amount3 = 0
    positive3 = 0
    negative3 = 0
    neutral3 = 0

    amount4 = 0
    positive4 = 0
    negative4 = 0
    neutral4 = 0

    amount5 = 0
    positive5 = 0
    negative5 = 0
    neutral5 = 0

    amount6 = 0
    positive6 = 0
    negative6 = 0
    neutral6 = 0

    amount7 = 0
    positive7 = 0
    negative7 = 0
    neutral7 = 0

    amount8 = 0
    positive8 = 0
    negative8 = 0
    neutral8 = 0

    amount9 = 0
    positive9 = 0
    negative9 = 0
    neutral9 = 0

    amount10 = 0
    positive10 = 0
    negative10 = 0
    neutral10 = 0

    amount11 = 0
    positive11 = 0
    negative11 = 0
    neutral11 = 0

    amount12 = 0
    positive12 = 0
    negative12 = 0
    neutral12 = 0
    for k, v in emotion_result.items():
        for m,n in v.items():
            if int(m) == 1:
                amount1 += n['amount']
                positive1 += n['positive']
                negative1 += n['negative']
                neutral1 += n['neutral']

            if int(m) == 2:
                amount2 += n['amount']
                positive2 += n['positive']
                negative2 += n['negative']
                neutral2 += n['neutral']

            if int(m) == 3:
                amount3 += n['amount']
                positive3 += n['positive']
                negative3 += n['negative']
                neutral3 += n['neutral']

            if int(m) == 4:
                amount4 += n['amount']
                positive4 += n['positive']
                negative4 += n['negative']
                neutral4 += n['neutral']

            if int(m) == 5:
                amount5 += n['amount']
                positive5 += n['positive']
                negative5 += n['negative']
                neutral5 += n['neutral']

            if int(m) == 6:
                amount6 += n['amount']
                positive6 += n['positive']
                negative6 += n['negative']
                neutral6+= n['neutral']

            if int(m) == 7:
                amount7 += n['amount']
                positive7 += n['positive']
                negative7+= n['negative']
                neutral7 += n['neutral']

            if int(m) == 8 :
                amount8 += n['amount']
                positive8 += n['positive']
                negative8 += n['negative']
                neutral8 += n['neutral']

            if int(m) == 9:
                amount9 += n['amount']
                positive9 += n['positive']
                negative9 += n['negative']
                neutral9 += n['neutral']

            if int(m) == 10:
                amount10 += n['amount']
                positive10 += n['positive']
                negative10 += n['negative']
                neutral10 += n['neutral']

            if int(m) == 11:
                amount11 += n['amount']
                positive11 += n['positive']
                negative11 += n['negative']
                neutral11 += n['neutral']

            if int(m) == 12:
                amount12 += n['amount']
                positive12 += n['positive']
                negative12 += n['negative']
                neutral12 += n['neutral']

    print("amount1 " + str(amount1) + " positive1 " + str(positive1) + " negative1 " + str(negative1) + " neutral1 " + str(neutral1))
    print("amount2 " + str(amount2) + " positive2 " + str(positive2) + " negative2 " + str(negative2) + " neutral2 " + str(neutral2))
    print("amount3 " + str(amount3) + " positive3 " + str(positive3) + " negative3 " + str(negative3) + " neutral3 " + str(neutral3))
    print("amount4 " + str(amount4) + " positive4 " + str(positive4) + " negative4 " + str(negative4) + " neutral4 " + str(neutral4))
    print("amount5 " + str(amount5) + " positive5 " + str(positive5) + " negative5 " + str(negative5) + " neutral5 " + str(neutral5))
    print("amount6 " + str(amount6) + " positive6 " + str(positive6) + " negative6 " + str(negative6) + " neutral6 " + str(neutral6))
    print("amount7 " + str(amount7) + " positive7 " + str(positive7) + " negative7 " + str(negative7) + " neutral7 " + str(neutral7))
    print("amount8 " + str(amount8) + " positive8 " + str(positive8) + " negative8 " + str(negative8) + " neutral8 " + str(neutral8))
    print("amount9 " + str(amount9) + " positive9 " + str(positive9) + " negative9 " + str(negative9) + " neutral9 " + str(neutral9))
    print("amount10 " + str(amount10) + " positive10 " + str(positive10) + " negative10 " + str(negative10) + " neutral10 " + str(neutral10))
    print("amount11 " + str(amount11) + " positive11 " + str(positive11) + " negative11 " + str(negative11) + " neutral11 " + str(neutral11))
    print("amount12 " + str(amount12) + " positive12 " + str(positive12) + " negative12 " + str(negative12) + " neutral1 " + str(neutral12))

    # write the result to a new data file in couchdb
    # couch.create('Month')
    # res_db = couch['Month']
    #
    # for city in emotion_result:
    #   city_json = dict()
    #   city_json[city] = emotion_result[city]
    #   res_db.save(city_json)

process_data()
