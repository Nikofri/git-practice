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

df_temp2025 = pd.DataFrame()
df_perc2025 = pd.DataFrame()

#adds data from 2025 to a dataframe
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    df_temp2025 = pd.concat([df_temp2025, row.iloc[0].to_frame().T], ignore_index=True)
    df_perc2025 = pd.concat([df_perc2025, row.iloc[2].to_frame().T], ignore_index=True)


endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '1925-01-01/1925-12-31',
}

r = requests.get(endpoint, parameters, auth=(client_id,''))
json = r.json()
data = json['data']

#adds data from 1925 to dataframe
df_1925 = pd.DataFrame()
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    df_1925 = pd.concat([df_1925, row], ignore_index=True)


def printer(data: pd.DataFrame) -> None:
    """
    Takes info from dataframe and prints it
    """
    info = {
    'mean':round(data['value'].mean(), 2), 
    'median': round(data['value'].median(), 2), 
    'max': round(data['value'].max(), 2), 
    'min': round(data['value'].min(), 2)
    }
    print(f'year: {data['referenceTime'][0][:4]}')
    for keys in info:
        print(f'{keys:<10}: {info[keys]:>9} C')

printer(df_1925)
printer(df_temp2025)

plt.plot(df_perc2025['referenceTime'], df_perc2025['value'], label='Percipitation')
plt.plot(df_temp2025['referenceTime'], df_temp2025['value'], label='Temperature 2025')
plt.plot(df_temp2025['referenceTime'], df_1925['value'], label='Temperature 1925')
plt.legend()
plt.grid()
plt.xticks([])
plt.xlabel('Date')
plt.ylabel('Temperature/Percipitation')
plt.show()

