import pymongo,time

client = pymongo.MongoClient('localhost',27017)
db_yac8 = client['yac8']
down_info = db_yac8['down']

while True:
    print(down_info.find().count())
    time.sleep(5)