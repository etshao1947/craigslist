import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option("display.max_columns", 20)

df = pd.read_csv(r'C:\Users\bshao\PycharmProjects\pachong\venv\dataset.csv', sep = '||', names = ['id', 'date', 'price', 'title', 'link'])

"""
df.date = pd.to_datetime(df.date)
df = df.sort_values(by=['date', 'id'], ascending=False)
df= df.drop_duplicates(subset=['id'])
df = df.drop_duplicates(subset=['title'])

print(df)
"""