import json
import couchdb
import re

couch = couchdb.Server('http://localhost:9000')
db = couch.create('twitter_db2')

newData = []
count = 0

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index + len(char)] == char:
                    return index

            index += 1

    return -1

with open('projecttest.json', 'r') as f:
    next(f)
    count = 0
    for line in f:
        count = count + 1
        print(count)
        try:
            data = json.loads(line[:-2])
            # print(data)

            Id = data['id']
            text = data['doc']['text']

            try:
                coordinates = data['doc']['coordinates']['coordinates']
                a = re.search('#GlenEira', text)
                b = re.search('#gleneira', text)
                c = re.search('#Gleneira', text)

                if ((a is not None) or (b is not None) or (c is not None)):
                    doc = {
                        'id': Id,
                        'content': {
                            'text': text,
                            'coordinates': coordinates
                        }
                    }
                    #print(doc)
                db.save(doc)

            except:
                print(" No Coordinates!!!!!")
                a = re.search('#GlenEira', text)
                b = re.search('#gleneira', text)
                c = re.search('#Gleneira', text)

                if ((a is not None) or (b is not None) or (c is not None)):
                    doc = {
                        'id': Id,
                        'content': {
                            'text': text,
                        }
                    }
                    #print("Hello")
                    #print(doc)

                db.save(doc)
        except:
           print("LLLLLLL")
           pass