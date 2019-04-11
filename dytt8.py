import requests
from bs4 import BeautifulSoup
from requests import ConnectionError

start_url = 'http://www.ygdy8.net/html/gndy/oumei/list_7_'
headers = {
    'Cookie': '37cs_user=37cs93439541818; 37cs_pidx=2; cscpvrich5041_fidx=2; 37cs_show=253%2C75',
    'Host': 'www.dytt8.net',
    'If-Modified-Since': 'Wed, 10 Apr 2019 18:15:12 GMT',
    'If-None-Match': "0f88a56c9efd41:320",
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def get_page(url):
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            res.encoding = 'gbk'
            return res.text
        else:
            return None
    except ConnectionError as e:
        print(e)
        pass

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    tbs = soup.select("div.co_content8 table")
    for tb in tbs:
        print(tb.get_text())


url = start_url+str(2)+'.html'
html = get_page(url)
parse_page(html)


'''
#header > div > div.bd2 > div.bd3 > div.bd3r > div.co_area2 > div.co_content8 > ul > table:nth-child(1)
'''