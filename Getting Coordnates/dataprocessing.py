import json
import couchdb
import re

#couch = couchdb.Server('http://localhost:9000')
#db = couch.create('twitter_db2')

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
    for line in f:
        try:
            start1 = find_str(line, "id")
            end1 = find_str(line, "key")

            start2 = find_str(line, "text")
            end2 = find_str(line, "is_quote_status")

            start3 = find_str(line, "coordinates")
            end3 = find_str(line, "entities")

            newId = line[start1 - 1:end1 - 2]
            newText = line[start2 - 1:end2 - 2]
            coordinates = line[start3 + 14:end3 - 2]
            start4 = find_str(coordinates, "coordinates")
            newCoordinates = coordinates[start4 - 1:-1]
            newline = "{" + newId + "," + newText + "," + newCoordinates + "}"
            newline = json.loads(newline)

            Id = newline['id']
            text = newline['text']
            coordinates = newline['coordinates']

            a = re.search('#Gleneiracouncil', text)
            b = re.search('#gleneiracouncil', text)
            c = re.search('#GlenEiraCouncil', text)
            d = re.search('#GLENEIRACOUNCIL', text)
            e = re.search('#gleneiracitycouncil', text)
            f = re.search('@gleneiracitycouncil', text)
            g = re.search('#GlenEiraCityCouncil', text)
            h = re.search('#Gleneiracitycouncil', text)
            i = re.search('@GlenEiraCityCouncil', text)
            j = re.search('@gleneiracouncil', text)

            if ((a is not None) or (b is not None) or (c is not None) or (d is not None) or (e is not None)
                    or (f is not None) or (g is not None) or (h is not None) or (i is not None) or (
                            j is not None)):
                doc = {
                    'id': Id,
                    'content': {
                        'text': text,
                        'coordinates': coordinates
                    }
                }
                #db.save(doc)
        except:
            print("ERROR!!!!!!!!")
            pass
