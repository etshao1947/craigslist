import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from joblib import Parallel, delayed


def get_site_add(search_var, key_words):
    link = 'https://geo.craigslist.org/iso/us'

    try:
        headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        response = urllib.request.Request(link, headers=headers)
        html = urllib.request.urlopen(response).read().decode('utf-8')

    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('error' + str(e.reason))
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print('errorCode' + str(e.code))

    soup = BeautifulSoup(html, 'html.parser')

    linkList = soup.find('ul', {'class': 'height6 geo-site-list'})
    linkList_item = linkList.find_all('a')

    siteList = []
    for item in linkList_item:
        link = (str(item['href']) + search_var + key_words)
        siteList.append(link)

    return siteList


def gen_data(link):

    global data

    try:
        headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        response = urllib.request.Request(link, headers=headers)
        html = urllib.request.urlopen(response).read().decode('utf-8')

    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('error' + str(e.reason))
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print('errorCode' + str(e.code))

    soup = BeautifulSoup(html,'html.parser')
    itemList = soup.find('ul', {'class': 'rows'})

    for item in itemList:
        try:
            name = item.find('a', {'class': 'result-title hdrlnk'}).get_text()
            price = item.find('span', {'class': 'result-price'}).get_text()
            date = item.find('time')['datetime']
            link = item.find('a', {'class': 'result-title hdrlnk'})['href']
            id = (str(link).split('/')[-1]).split('.')[0]
            data = {'id':[id], 'date':[date], 'price':[price], 'name': [name], 'link':[link]}

            print(data)

        except:
            pass

    return str(data)




key_words = 'japanese+sword'
search_var = '/search/sss?query='
siteList = get_site_add(search_var, key_words)

data = None

dataset = Parallel(n_jobs=2, backend='threading', verbose=0)(delayed(gen_data)(link) for link in siteList[0:4])

print(dataset)
print(len(dataset))