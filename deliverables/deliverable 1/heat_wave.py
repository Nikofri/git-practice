import pandas as pd
import requests

with open('client-ID.txt', 'r') as file:
    for line in file:
        client_id = line
file.close()

endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'max(air_temperature P1D)',
    'referencetime': '2018-01-01/2018-12-31',
}

r = requests.get(endpoint, parameters, auth=(client_id,''))
json = r.json()
data = json['data']

df = pd.DataFrame()
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['sourceId'] = data[i]['sourceId']
    row['referenceTime'] = data[i]['referenceTime']
    if len(row) >= 2:
        row.loc[row.index[0], 'value'] = (row['value'].iloc[0] + row['value'].iloc[1]) / 2
    df = pd.concat([df, row.iloc[0:1]], ignore_index=True)


def heat_wave_scan(data):
    heat = []
    x = 0
    for i in range(len(data)):
        if data['value'][i] >= 27:
            x += 1
        else:
            if x >= 5:
                heat.append([data['referenceTime'][i-x][:10], data['referenceTime'][i-1][:10]])
            x = 0

    try:
        with open('heatwave_summary.yml', 'a', encoding='utf-8') as file:
            file.write('dates:\n')
            for i in heat:
                file.write(f'- {i[0]} - {i[1]}\n')
            file.write(f'''station_id : {data['sourceId'][0][:7]}
year: {heat[0][0][:4]}
''')
        file.close()
    except FileExistsError:
        with open('heatwave:summary.yml', 'a', encoding='utf-8') as file:
            file.write('dates:\n')
            for i in heat:
                file.write(f'- {i[0]} - {i[1]}\n')
            file.write(f'''station_id : {data['sourceId'][0][:7]}
year: {heat[0][0][:4]}
''')
        file.close()

heat_wave_scan(df)