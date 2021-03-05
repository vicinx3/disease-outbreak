import requests
import json
from pymongo import MongoClient
# Store data from API request in temp file

# cv_response = requests.put('https://www.codeonavirus.com/who/articles', json = {"start_date":"1996-01-01", "end_date": "2020-05-31"})
# fp = open('results.json', 'w')
# json.dump(cv_response.json(), fp)
# fp.close()

# https://codeonavirus.com/
def fetch_WHO():
    print("Fetching articles from WHO...")
    url = r'https://codeonavirus.com/who/articles'
    query = {
        'start_date': '1996-01-01',
        'end_date': '2030-12-31'
    } 
    response = requests.put(url, json=query)
    if response.status_code != 200: 
        return []
    articles = response.json()
    return articles

# https://app.swaggerhub.com/apis-docs/SMEZ1234/SENG3011-CalmClams/1.0.0#/API%20endpoint
'''
def fetch_GIM():
    print("Fetching articles from Global Incident Map...")
    url = r'http://calmclams.appspot.com/disease_reports'
    query = {
        'start_date': '1996-01-01T00:00:00',
        'end_date': '2030-12-31T00:00:00'
    }
    response = requests.get(url, params=query)
    if response.status_code != 200: 
        return []
    articles = response.json()['articles']
    return articles
'''

# https://app.swaggerhub.com/apis-docs/s3ngin3/outbreaks/1.0.0-oas3#/default/searchArticles

def fetch_ProMED():
    print("Fetching articles from ProMED...")
    url = r'http://sengine.online/article'
    query = {
        'start': '1996-01-01T00:00:00',
        'end': '2030-12-31T00:00:00',
        'n': 999999
    }
    response = requests.get(url, params=query)
    if response.status_code != 200: 
        return []
    articles = response.json()
    return articles

'''
fp = open('results.json', 'w')
a = fetch_WHO() + fetch_ProMED()# + fetch_GIM()
print("Fetched %d articles" %(len(a)))
json.dump(a, fp)
fp.close()
'''

client = MongoClient('mongodb+srv://codeonavirus:codeonavirus@codeonavirus-etwjy.mongodb.net/test?retryWrites=true&w=majority')
db = client.app_database
articles = db.articles

print("Fetching articles from WHO...")

pipeline = [
    {'$match': {'source': 'WHO'}},
    {'$project': {'_id': 0, 'headline': 1, 'main_text': 1, 'reports': 1}}
]

WHO_articles = list(articles.aggregate(pipeline))

with open('results.json', 'w') as fp:
    json.dump(WHO_articles, fp)