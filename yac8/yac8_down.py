# -*- coding:gbk -*-

from bs4 import BeautifulSoup
import requests
import pymongo
from multiprocessing import Pool
import urllib.request,os,sys


client = pymongo.MongoClient('localhost',27017)
db_yac8 = client['yac8']
page_info = db_yac8['info']
down_info = db_yac8['down']


headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}



def down_img(img_link,img_path):
    try:
        filename = img_path + img_link[-16:]
        print("Begin Download: "+img_link+" Save to: "+filename)  # 打印下载信息
        urllib.request.urlretrieve(img_link, filename)  # 下载图片
    except Exception as er:
        print(er)
        pass

def open_link(num):
    for item in page_info.find({'num':num}):
        title = item['title']
        channel = item['channel']
        content = item['content']
        mark = item['mark']
        links = item['link']

        folder=channel+'/'
        if not os.path.isdir(folder):
            os.makedirs(folder)
        folder2=folder+title.replace(':','').replace('"','').replace('*','')[:16]+'/'
        if not os.path.isdir(folder2):
            os.makedirs(folder2)
        print(num,title,'\n==================================\n')
        img_text_name = str(num)+'.txt'
        img_text = title+'\n'+' '.join(mark)+'\n'+content
        try:
            f = open(folder2+img_text_name,'w')
            f.write(img_text)
            f.close()
            down_info.insert_one({'downnum': num})
            for link in links:
                try:
                    down_img(link, folder2)
                except Exception as e:
                    print(e)
                    pass
        except Exception as err:
            print(err)
            pass
page_num = [pnum['num'] for pnum in page_info.find()]
down_num = [item['downnum'] for item in down_info.find()]

x = set(page_num)
y = set(down_num)
rest_of_urls = list(x-y)

if __name__ == '__main__':
    pool = Pool()
    pool.map(open_link,rest_of_urls)

