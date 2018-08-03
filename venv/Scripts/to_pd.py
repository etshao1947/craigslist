import pandas as pd
pd.set_option('display.width', 10000)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 300)

df = pd.read_csv(r'C:\Users\bshao\PycharmProjects\pachong\venv\dataset.csv', sep = '|', names = ['id', 'date', 'price', 'title', 'link'], encoding='cp1252')

df.date = pd.to_datetime(df.date)
df = df.sort_values(by=['date', 'id'], ascending=False)
df= df.drop_duplicates(subset=['id'])
df = df.drop_duplicates(subset=['title'])

f = open('../result.html', 'a')

for index, row in df.iterrows():
    html = """
    <li>
        {}	|	{}	|	{}	|
        <a href="{}">{}</a>
    </li>
    """.format(row['date'], row['id'], row['price'], row['link'], row['title'])

    f.write('\n' + html)

    print(html)

f.close()