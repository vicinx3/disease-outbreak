import requests 
import json 
from db import db_insert, db_drop

# Codeonavirus WHO
def fetch_WHO():
    url = r'https://codeonavirus.com/who/articles'
    query = {
        'start_date': '1996-01-01',
        'end_date': '2030-12-31'
    } 
    response = requests.put(url, json=query)
    if response.status_code != 200: 
        return 
    content = response.json()
    i = 0
    for article in content: 
        db_insert('WHO', article, r'%Y-%m-%d')
        i += 1
        if i % 1000 == 0:
            print("Fetched %d articles" % (i))
    print("Fetched %d articles" % (i))

def fetch_JHU():
    pass

# CalmClams Global Incident Map
def fetch_GIM():
    url = r'http://calmclams.appspot.com/disease_reports'
    query = {
        'start_date': '1996-01-01T00:00:00',
        'end_date': '2030-12-31T00:00:00'
    }
    response = requests.get(url, params=query)
    if response.status_code != 200: 
        return 
    content = response.json()
    i = 0
    for article in content['articles']:
        date = article['date_of_publication']
        article['date_of_publication'] = date.split()[0]
        db_insert('GIM', article, r'%Y-%m-%d') 
        i += 1
        if i % 1000 == 0:
            print("Fetched %d articles" % (i))
    print("Fetched %d articles" % (i))

# SENGINE 3.0 ProMED
def fetch_ProMED():
    url = r'http://sengine.online/article'
    query = {
        'start': '1996-01-01T00:00:00',
        'end': '2030-12-31T00:00:00',
        'n': 999999
    }
    response = requests.get(url, params=query)
    if response.status_code != 200: 
        return 
    content = response.json()
    i = 0
    for article in content:
        db_insert('ProMED', article)
        i += 1
        if i % 1000 == 0:
            print("Fetched %d articles" % (i))
    print("Fetched %d articles" % (i))

if __name__ == '__main__':
    db_drop()
    print("Fetching WHO ...")
    fetch_WHO()
    # print("Fetching GIM ...")
    # fetch_GIM()
    print("Fetching ProMed ... ")
    fetch_ProMED()
    print("Update complete")