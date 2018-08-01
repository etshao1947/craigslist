import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import pandas as pd

pd.set_option('display.width',300)



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







key_words = 'japanese+sword'
search_var = '/search/sss?query={}'.format(key_words)
df_final = pd.DataFrame()

i=1
for item in siteList:
    print( str((i/len(siteList))*100) + '%...............................................')
    link = str(item + search_var)
    print(link)
    i += 1



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

    x = soup.find('ul', {'class': 'rows'})
    children = x.findChildren



    for item in x:
        try:
            name = item.find('a', {'class': 'result-title hdrlnk'}).get_text()

            price = item.find('span', {'class': 'result-price'}).get_text()

            date = item.find('time')['datetime']

            link = item.find('a', {'class': 'result-title hdrlnk'})['href']

            id = (str(link).split('/')[-1]).split('.')[0]

            data = {'id':[id], 'date':[date], 'price':[price], 'name': [name], 'link':[link]}
            print(data)

            df = pd.DataFrame.from_dict(data)
            df_final = df_final.append(df)

            print('===============================\n')
        except:
            pass


print(df_final)
df_final.to_csv(r'C:\Users\bshao\Downloads\craig_jp_sword.txt', header = None, index = None)
























