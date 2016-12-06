import pymongo,time

client = pymongo.MongoClient('localhost',27017)
db_yac8 = client['yac8']
page_info = db_yac8['info']

while True:
    print(page_info.find().count())
    time.sleep(5)