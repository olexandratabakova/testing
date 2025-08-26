import pandas as pd


df = pd.read_json('../texts_result/relations.json')
df = df[['person1', 'person2']]
print(df)
