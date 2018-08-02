import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import pandas as pd
from joblib import Parallel, delayed

pd.set_option('display.width',300)


def get_all_site_add():
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
        siteList.append(str(item['href']))

    return siteList



def gen_link(self, key_words):
    search_var = '/search/sss?query='
    link = str(self+search_var+key_words)
    return link



def get_listing_item(link):
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
    return itemList




def gen_data(item):

    global pf

    try:
        name = item.find('a', {'class': 'result-title hdrlnk'}).get_text()
        price = item.find('span', {'class': 'result-price'}).get_text()
        date = item.find('time')['datetime']
        link = item.find('a', {'class': 'result-title hdrlnk'})['href']
        id = (str(link).split('/')[-1]).split('.')[0]

        data = {'id': [id], 'date': [date], 'price': [price], 'name': [name], 'link': [link]}
        pf  = pd.dataframe.from_dict(data)
        print(pf)

    except:
        pass

    return pf




def pipeline(site, key_words):

    link = gen_link(site, key_words)
    itemList = get_listing_item(link)
    for item in itemList:
        dataset = gen_data(item)
        final_pf = final_pf.append(dataset)

    return final_pf








siteList = ['https://washingtondc.craigslist.org', 'https://chicago.craigslist.org']
key_words = 'japanese+sword'
#siteList = get_all_site_add()
pf = None
final_pf = pd.DataFrame()

x= Parallel(n_jobs=4, backend="threading", verbose=10)(delayed(pipeline)(site, key_words) for site in siteList)

print(x)



#df = pd.DataFrame.from_dict(data)
#df_final = df_final.append(df)
#print(df_final)
#df_final.to_csv(r'C:\Users\bshao\Downloads\craig_jp_sword.txt', header = None, index = None)
























