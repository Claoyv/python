# yac8: http://yac8.com/news/7512.html-13470.html
# -*- coding:gbk -*-
from bs4 import BeautifulSoup
import requests,random
import pymongo
from multiprocessing import Pool


client = pymongo.MongoClient('localhost',27017)
db_yac8 = client['yac8']
page_info = db_yac8['info']


headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}

proxy_list='''
http://122.96.59.105:82
http://122.72.32.73:80
http://122.96.59.98:80
http://122.96.59.107:843
http://124.88.67.17:82
http://122.7.154.245:8888
http://27.8.60.89:8888
http://218.103.42.101:1080
http://121.193.143.249:80
http://106.75.47.141:80
http://113.234.200.120:8888
http://183.129.151.130:80
http://123.56.74.13:8080
http://61.160.190.34:8088
http://113.195.94.151:8888
http://222.33.192.238:8118
http://27.151.220.130:8888
http://124.88.67.63:80
http://202.171.253.72:80
http://122.96.59.99:80
http://60.21.209.114:8080
http://60.194.100.51:80
http://120.76.203.31:80
http://121.61.100.58:8118
http://115.204.41.213:8118
http://202.108.2.42:80
http://106.75.176.4:80
http://218.25.13.23:80
http://101.53.101.172:9999
http://27.184.135.181:8888
http://120.92.3.165:80
http://122.193.14.106:82
http://60.26.99.43:8888
http://120.69.13.1:8888
http://39.64.89.80:8118
http://122.228.182.10:80
http://123.170.10.93:8888
http://120.76.243.40:80
http://114.237.84.211:8118
http://110.73.40.158:8123
http://121.204.165.177:8118
http://117.28.255.84:80
http://121.40.108.76:80
http://120.25.105.45:81
http://58.208.235.194:808
http://1.169.69.113:8080
http://60.30.26.119:8088
http://175.42.45.167:8888
http://139.196.108.68:80
http://115.28.2.233:8088
http://115.28.32.191:8081
http://124.42.7.103:80
http://125.109.75.211:3128
http://182.44.61.204:8888
http://119.10.72.34:80
http://122.228.179.178:80
http://106.75.47.29:80
'''

proxies={'http':random.choice(proxy_list.split())}

def get_info(num):
    url='http://www.yac8.com/news/'+str(num)+'.html'
    img_links=[]
    try:
#        wb_data=requests.get(url,headers=headers,proxies=proxies)
        wb_data=requests.get(url,headers=headers)
        wb_data.encoding='gbk'
        soup=BeautifulSoup(wb_data.text,'lxml')


        title=soup.select('div.a > h1')[0].text if soup.select('div.a > h1') else soup.title.text
        images=soup.select('#newsContent img')
        note=soup.select('div.note')[0].text if soup.select('div.note') else None
        pages=int(soup.select('table.pageNavBox.list a')[-2].text.replace('.','')) if soup.select('table.pageNavBox.list') else None
        channel=soup.select('#newsContent > div > div > a')[0].text if soup.select('#newsContent > div > div > a') else '其他书法'
#        channel='其他书法'
        marks=soup.select('div.mark > a') if soup.select('div.mark') else None

        for image in images:
            img_link = image.get('src')
            if img_link.startswith('..'):
                img_link = 'http://www.yac8.com' + img_link[2:]
            img_links.append(img_link)

        if marks != None:
            mark_list=[]
            for get_mark in marks:
                mark = get_mark.get_text()
                mark_list.append(mark)
        else:
            mark_list=[]
        if pages != None:
            for p in range(2,pages+1):
                page_url = 'http://www.yac8.com/news/'+str(num)+'_'+str(p)+'.html'

                try:
                    page_data = requests.get(page_url, headers=headers)
                    page_data.encoding = 'gbk'
                    page_soup = BeautifulSoup(page_data.text, 'lxml')
                    page_imgs = page_soup.select('#newsContent img')
                    for page_img in page_imgs:
                        p_link = page_img.get('src')
                        if p_link.startswith('..'):
                            p_link = 'http://www.yac8.com'+p_link[2:]
#                        print(p_link)
                        img_links.append(p_link)

                except Exception as pe:
                    print(pe)
        if img_links !=[]:
            print(num,pages,title,channel,mark_list,' Saved! ',sep=' | ')
            page_info.insert_one({'num':num,'title':title,'link':img_links,'content':note,'channel':channel,'mark':mark_list})

    except Exception as e:
        print(e)

page_num = list(range(1,11030))
db_urls = [item['num'] for item in page_info.find()]

y = set(db_urls)
x = set(page_num)
rest_of_urls = list(x-y)


if __name__ == '__main__':
    pool = Pool()
    pool.map(get_info,rest_of_urls)

# get_info(11030)