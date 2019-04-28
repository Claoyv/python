from bs4 import BeautifulSoup
import requests
import pymongo
import urllib.request,time


# client = pymongo.MongoClient('80.80.1.80',27017)
# db = client['spider']
# tb = db['qbs']


headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive',
    'Host': 'tieba.baidu.com',
}


def down_img(link):
    try:
        time.sleep(2)
        res=requests.get(link,headers=headers)
#        res.encoding='utf-8'
        soup=BeautifulSoup(res.text,'lxml')
        imgs=soup.select('img.BDE_Image')
        print(link)
        for img in imgs:
            filename="d:/cyz/"+img['src'][-13:]
            print("Begin Download: "+ img['src'] +" Save to: "+filename)  
            urllib.request.urlretrieve(img['src'], filename) 

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    for i in range(6):
        link = 'https://tieba.baidu.com/p/3131550054?pn='+str(i)
        down_img(link)


# get_info(11030)


'''
http://gaoqing.3zitie.cn/research.asp?page=21&searchkey=%E9%BD%90%E7%99%BD%E7%9F%B3&action=1&categoryid=&jiage=0
http://gaoqing.3zitie.cn/research.asp?action=21&searchkey=%E9%BD%90%E7%99%BD%E7%9F%B3&&action=1&categoryid=&jiage=0
'''