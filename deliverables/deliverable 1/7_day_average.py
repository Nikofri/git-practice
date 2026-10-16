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
    'referencetime': '2018-01-01/2018-12-31',
}

r = requests.get(endpoint, parameters, auth=(client_id,''))
json = r.json()
data = json['data']
df = pd.DataFrame()

for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    df = pd.concat([df, row.iloc[0].to_frame().T], ignore_index=True)


def average(data):
    averages = []
    dates = []
    current = []
    for i in range(len(data)):
        current.append(data['value'].iloc[i])
        if len(current) == 7:
            averages.append(sum(current) / 7)
            dates.append(data['referenceTime'].iloc[i-6])
            current.pop(0)

    return averages, dates

plt.plot(df['referenceTime'], df['value'], 'o', label='Temperature')
plt.plot(average(df)[1], average(df)[0], label='7 day average')
plt.legend()
plt.grid()
plt.xticks([])
plt.show()
