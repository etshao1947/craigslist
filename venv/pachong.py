import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import pandas as pd
pd.set_option('display.width', 10000)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 300)


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

    f = open('dataset.csv', 'a')

    for item in itemList:
        try:
            name = item.find('a', {'class': 'result-title hdrlnk'}).get_text()
            price = item.find('span', {'class': 'result-price'}).get_text()
            date = item.find('time')['datetime']
            link = item.find('a', {'class': 'result-title hdrlnk'})['href']
            id = (str(link).split('/')[-1]).split('.')[0]

            #data = {'id': id, 'date': date, 'price': price, 'title': name, 'link': link}

            data = str(id +'|'+ date  +'|'+ price +'|'+ name  +'|'+ link)
            print(data)

            f.write('\n' + data)


        except:
            pass
    f.close()


def get_key_words():
    search = str(input()).split(' ')
    key_words = '+'.join(search)
    return key_words


key_words = get_key_words()
search_var = '/search/sss?query='
siteList = get_site_add(search_var, key_words)
dataset = None



Parallel(n_jobs=-1, backend='threading', verbose=10)(delayed(gen_data)(link) for link in siteList)





df = pd.read_csv('dataset.csv', sep = '|', names = ['id', 'date', 'price', 'title', 'link'], encoding='cp1252')
df.date = pd.to_datetime(df.date)
df = df.sort_values(by=['date', 'id'], ascending=False)
df= df.drop_duplicates(subset=['id'])
df = df.drop_duplicates(subset=['title'])

f = open('result.html', 'a')

for index, row in df.iterrows():
    html = """
    <li>
        {}	|	{}	|	{}	|
        <a href="{}">{}</a>
    </li>
    """.format(row['date'], row['id'], row['price'], row['link'], row['title'])

    f.write('\n' + html)

    #print(html)

f.close()

print('========================= done ========================')