import json

import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///../data/database_br.db')


with open('ingestions_br.json', 'r') as open_file:
    ingestions = json.load(open_file)

# breakpoint()
for item in ingestions:
    df = pd.read_csv(item['path'], encoding='latin-1', sep=';')
    df.to_sql(item['table'], engine, if_exists='replace', index=False)
