import json
import datetime
from pprint import pprint
from db import prettify_disease, convert_code
# Processing 

f = open('Prediction/predicted_outbreaks.json')
content = json.load(f)
f.close()

epoch = datetime.datetime(2020, 5, 1)

outbreaks = []
for country in content: 
    for disease in content[country]:
        date = datetime.datetime.strptime(content[country][disease]['date'], r'%Y-%m-%d')
        offset = (date.year - epoch.year) * 12 + (date.month - epoch.month) 
        outbreaks.append({
            'disease': disease,
            'duration': content[country][disease]['duration'], 
            'country': country,
            'date': date,
            'offset': offset
        })

outbreaks = list(filter(lambda x: x['offset'] < 31, outbreaks))
outbreaks.sort(key=lambda x: x['date'])

# Functions 

def get_outbreaks_by_country(offset, country, disease): 
    filtered = list(filter(lambda x: x['offset'] == offset, outbreaks))
    if country != '': 
        filtered = list(filter(lambda x: x['country'] == country, filtered))
    if disease != '':
        filtered = list(filter(lambda x: x['disease'] == disease, filtered))

    result = {}
    for x in filtered: 
        if x['country'] in result: 
            result[x['country']] += 1
        else:
            result[x['country']] = 1
    return result

def get_outbreaks(prettify=False):
    def formatter(x):
        return {
            'country': x['country'],
            'date': x['date'].strftime(r'%Y-%m-%d'),
            'disease': x['disease'],
            'duration': x['duration']
        }
    return list(map(formatter, outbreaks))