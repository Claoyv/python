import requests,urllib.request,time
from bs4 import BeautifulSoup

url = 'http://www.qu.la/book/197/'
folder = '/oldfish/197/'

def get_links(url):
    pages=[]
    web_data = requests.get(url)
    web_data.encoding='gbk'
    soup = BeautifulSoup(web_data.text,'lxml')
    links = soup.select('#list > dl > dd > a')
    for link in links:
#        title = link.text
        page = url+link['href']
        pages.append(page)
    return(pages)

def get_pages(page,no):
    time.sleep(1)
    page_data = requests.get(page)
    page_data.encoding ='gbk'

    page_soup = BeautifulSoup(page_data.text,'lxml')
    title = str(no)+page_soup.title.text.split('_')[0]
    text = page_soup.select('#content')[0].text
    newtext = text.replace('    ','\n    ')
    try:
        f = open(folder+title+'.txt','w')
        f.write(newtext)
        f.close()
        print(title+' ==> Saved. OK!')
    except UnicodeEncodeError as e:
        print(title+'Unicode Error...')
def main():
    i=0
    links=get_links(url)
    for link in links:
        get_pages(link,i)
        i+=1

main()
#get_pages('http://www.qu.la/book/197/154117.html',136)

