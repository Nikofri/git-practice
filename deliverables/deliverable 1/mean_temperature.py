import matplotlib.pyplot as plt
import pandas as pd
import requests

with open('client-ID.txt', 'r') as file:
    for line in file:
        client_id = line
file.close()

endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r = requests.get(endpoint, parameters, auth=(client_id,''))
json = r.json()
data = json['data']
df = pd.DataFrame()

for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    df = pd.concat([df, row], ignore_index=True)






info = {
    'mean': round(df.loc[:, 'value'].mean(), 2), 
    'median': round(df.loc[:, 'value'].median(), 2), 
    'max': round(df.loc[:, 'value'].max(), 2), 
    'min': round(df.loc[:, 'value'].min(), 2)
    }

for keys in info:
    print(f'{keys:<10}: {info[keys]:>9} C')

plt.plot(df['referenceTime'], df['value'])
plt.xticks([])
plt.xlabel('date')
plt.ylabel('temperature')
plt.show()

