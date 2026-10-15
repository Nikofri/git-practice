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
    'elements': 'mean(air_temperature P1D), sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r = requests.get(endpoint, parameters, auth=(client_id,''))
json = r.json()
data = json['data']

df_temp = pd.DataFrame()
df_perc = pd.DataFrame()

for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    df_temp = pd.concat([df_temp, row.iloc[0].to_frame().T], ignore_index=True)
    df_temp = pd.concat([df_temp, row.iloc[1].to_frame().T], ignore_index=True)
    df_perc = pd.concat([df_perc, row.iloc[2].to_frame().T], ignore_index=True)
    df_perc = pd.concat([df_perc, row.iloc[3].to_frame().T], ignore_index=True)

info = {
    'mean':round(df_temp['value'].mean(), 2), 
    'median': round(df_temp['value'].median(), 2), 
    'max': round(df_temp['value'].max(), 2), 
    'min': round(df_temp['value'].min(), 2)
    }




for keys in info:
    print(f'{keys:<10}: {info[keys]:>9} C')

plt.plot(df_perc['referenceTime'], df_perc['value'], label='Percipitation')
plt.plot(df_temp['referenceTime'], df_temp['value'], label='Temperature')
plt.legend()
plt.grid()
plt.xticks([])
plt.xlabel('Date')
plt.ylabel('Temperature/Percipitation')
plt.show()

