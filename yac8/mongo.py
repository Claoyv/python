# -*- coding:gbk -*-
from bs4 import BeautifulSoup
import requests,random
import pymongo
from multiprocessing import Pool


client = pymongo.MongoClient('localhost',27017)
db_yac8 = client['yac8']
page_info = db_yac8['info']

for item in page_info.find().limit(300):
    print(item['title'])