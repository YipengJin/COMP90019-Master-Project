from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
import couchdb
import re

# couch = couchdb.Server('http://localhost:9000')
# db = couch.create('twitter_db2')

with open('gleneirapolygon.json','r') as f:
    for lines in f:
        data = json.loads(lines)
        polygon_area = Polygon(data['geometries'][0]['coordinates'][0][0])

newData = []
count = 0

with open('projecttest.json', 'r') as f:
    next(f)
    count = 0
    for line in f:
        count = count + 1
        print(count)
        try:
            data = json.loads(line[:-2])

            Id = data['id']
            text = data['doc']['text']

            try:
                coordinates = data['doc']['coordinates']['coordinates']
                point = Point(coordinates[0],coordinates[1])
                polygon = polygon_area


                if (polygon.contains(point) is True):
                    print(111111)
                    doc = {
                        'id': Id,
                        'content': {
                            'text': text,
                            'coordinates': coordinates
                        }
                    }
                    # db.save(doc)

            except:
                print(" No Coordinates!!!!!")
                pass
        except:
           print("LLLLLLL")
           pass


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
import couchdb
import re

couch = couchdb.Server('http://localhost:5984')
db = couch.create('poly2018')

with open('gleneirapolygon.json','r') as f:
    for lines in f:
        data = json.loads(lines)
        polygon_area = Polygon(data['geometries'][0]['coordinates'][0][0])

newData = []
count = 0

with open('melbourne-2018-twitter.json', 'r') as f:
    next(f)
    count = 0
    for line in f:
        count = count + 1
        print(count)

        try:
            data = json.loads(line[:-2])

            Id = data['id']
            text = data['doc']['text']

            try:
                coordinates = data['doc']['coordinates']['coordinates']
                point = Point(coordinates[0],coordinates[1])
                polygon = polygon_area


                if (polygon.contains(point) is True):
                    print(111111)
                    doc = {
                        'id': Id,
                        'content': {
                            'text': text,
                            'coordinates': coordinates
                        }
                    }
                    db.save(doc)

            except:
                print(" No Coordinates!!!!!")
                pass
        except:
           print("LLLLLLL")
           pass
