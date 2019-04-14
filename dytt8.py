import requests
from bs4 import BeautifulSoup
from requests import ConnectionError
import pymongo
import re

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn['dytt8']
col = db['links']
info = db['oumei']

start_url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_'
headers = {
    'Host' : 'www.ygdy8.net',
    'Cookie': 'XLA_CI=de20a1b885809f3e6948880351946037; 37cs_pidx=1; 37cs_user=37cs20186332737; 37cs_show=253; cscpvrich5041_fidx=1',
    'If-None-Match' : '80c22a641f2d41:73a',
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}


def get_page(url):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            res.encoding = 'gbk'
            return res.text
        else:
            return None
    except ConnectionError as e:
        print(e)
        pass


def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    tbs = soup.select("b > a:nth-of-type(2)")
    for tb in tbs:
        link = tb.get('href')
        col.insert_one({'link': link})

#   print(link + 'saved!')


def get_info(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    cNamePatt = re.compile('◎译.*?名(.*?)<br />◎', re.S)
    eNamePatt = re.compile('◎片.*?名(.*?)<br />◎', re.S)
    yearPatt = re.compile('◎年.*?代(.*?)<br />◎', re.S)
    earePatt = re.compile('◎产.*?地(.*?)<br />◎', re.S)
    typesPatt = re.compile('◎类.*?别(.*?)<br />◎', re.S)
    lanPatt = re.compile('◎语.*?言(.*?)<br />◎', re.S)
    imdbPatt = re.compile('◎IMDb评分(.*?)<br />◎', re.S)
    doubanPatt = re.compile('◎豆瓣评分(.*?)<br />◎', re.S)
    daoyanPatt = re.compile('◎导.*?演(.*?)<br />◎', re.S)
    actorPatt = re.compile('◎主.*?演(.*?)<br />◎', re.S)
    aboutPatt = re.compile('◎简.*?介(.*?)<img', re.S)
    linkPatt = re.compile('ftp://(.*?)">ftp://',re.S)
    


    cname = re.findall(cNamePatt, res.text)[0].strip() if re.findall(cNamePatt, res.text) else None
    ename = re.findall(eNamePatt, res.text)[0].strip() if re.findall(eNamePatt, res.text) else None
    years = re.findall(yearPatt, res.text)[0].strip() if re.findall(yearPatt, res.text) else None
    eare = re.findall(earePatt, res.text)[0].strip() if re.findall(earePatt, res.text) else None
    types = re.findall(typesPatt, res.text)[0].strip() if re.findall(typesPatt, res.text) else None
    lan = re.findall(lanPatt, res.text)[0].strip() if re.findall(lanPatt, res.text) else None
    imdb = re.findall(imdbPatt, res.text)[0].strip() if re.findall(imdbPatt, res.text) else None
    douban = re.findall(doubanPatt, res.text)[0].strip() if re.findall(doubanPatt, res.text) else None
    daoyan = re.findall(daoyanPatt, res.text)[0].strip().replace('&middot;','.') if re.findall(daoyanPatt, res.text) else None
    actor = re.findall(actorPatt, res.text)[0].strip().replace('&middot;','.') if re.findall(actorPatt, res.text) else None
    about = re.findall(aboutPatt, res.text)[0].strip() if re.findall(aboutPatt, res.text) else None
    link = re.findall(linkPatt,res.text)[0].strip() if re.findall(linkPatt,res.text) else None

    print(res.text,cname, ename,years,eare,types,lan,imdb,douban,daoyan,actor,about,link)


def main():
    for i in range(1, 214):
        url = start_url + str(i) + '.html'
        html = get_page(url)
        print("start the page: " + url)
        parse_page(html)


if __name__ == "__main__":
    #main()
    get_info('http://www.ygdy8.net/html/gndy/dyzz/20190403/58404.html')
'''
#header > div > div.bd2 > div.bd3 > div.bd3r > div.co_area2 > div.co_content8 > ul > table:nth-child(1)
#header > div > div.bd2 > div.bd3 > div.bd3r > div.co_area2 > div.co_content8 > ul > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2) > b > a:nth-child(2)
'''