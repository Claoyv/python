# yac8: http://yac8.com/news/7512.html-13470.html
# -*- coding:gbk -*-
from bs4 import BeautifulSoup
import requests
import pymongo
#from multiprocessing import Pool
import urllib.request,time


client = pymongo.MongoClient('80.80.1.80',27017)
db = client['spider']
tb = db['qbs']


headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive',
    'cookie' :'ASPSESSIONIDQQSDSRSA=FNNJPAIDBPEPLELJLOMDMFMH; usercookies=20190424160749938375; __51cke__=; __tins__4997368=%7B%22sid%22%3A%201556095306288%2C%20%22vd%22%3A%2013%2C%20%22expires%22%3A%201556097526533%7D; __51laig__=16; Hm_lvt_83e7bd7ca189b67f1e59d69f2a16ce30=1556095448,1556095570,1556095593,1556095727; Hm_lpvt_83e7bd7ca189b67f1e59d69f2a16ce30=1556095727',
    'Host': 'gaoqing.3zitie.cn',
    'Cache-Control': 'max-age=0',
}

def get_link(num):
    url = url='http://gaoqing.3zitie.cn/research.asp?page='+str(num)+'&searchkey=%E9%BD%90%E7%99%BD%E7%9F%B3&jiage=0'
    try:
#        wb_data=requests.get(url,headers=headers,proxies=proxies)
        res=requests.get(url,headers=headers)
        res.encoding='utf-8'
        soup=BeautifulSoup(res.text,'lxml') 
        links=soup.select("#wrapper > div > div > div > div > div:nth-of-type(1) > a")
        titles=soup.select("#wrapper > div > div > div > div > div:nth-of-type(1) > a > img")
        for link,title in zip(links,titles):
            tb.insert_one({"title":title["title"],"link":link["href"],"dmark":0})
        print(url,"saved!")
    except Exception as e:
        print(e)




def down_img(id,link,title):
    try:
        time.sleep(2)
        url = 'http://gaoqing.3zitie.cn'+link
        res=requests.get(url,headers=headers)
        res.encoding='utf-8'
        soup=BeautifulSoup(res.text,'lxml')
        img=soup.find('img')
        filename = 'qbs/' + str(title) +'.jpg'
        print("Begin Download: "+ img['src'] +" Save to: "+filename)  
        urllib.request.urlretrieve(img['src'], filename) 
        tb.update_one({"_id":id},{"$set":{"dmark":1}})
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    for item in tb.find({'dmark':0}):
        id = item['_id']
        link =  item['link']
        title = item['title']
        down_img(id,link,title)


# get_info(11030)


'''
http://gaoqing.3zitie.cn/research.asp?page=21&searchkey=%E9%BD%90%E7%99%BD%E7%9F%B3&action=1&categoryid=&jiage=0
http://gaoqing.3zitie.cn/research.asp?action=21&searchkey=%E9%BD%90%E7%99%BD%E7%9F%B3&&action=1&categoryid=&jiage=0
'''