# Preprocess data fetched from articles, write results into csv and alert if new diseases

import json
import csv
import re
from datetime import date
from os import path
from pymongo import MongoClient

# Check results.json exists
# if not path.exists('results.json'):
#    print("Please run python3 data_api.py first")
#    exit()

# Clear existing csv data, add headings
with open('disease_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['disease'] + ['days since last outbreak'] + ['year started'] + ['event_days'] + ['country'] + ['n_reports'] + ['outbreak'])

# JSON results from API
with open('results.json', 'r') as json_fp:
     articles = json.load(json_fp)

# Fetch data

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

print("Fetching articles from ProMED...")

pipeline = [
    {'$match': {'source': 'ProMED'}},
    {'$project': {'_id': 0, 'headline': 1, 'main_text': 1, 'reports': 1}}
]

ProMED_articles = list(articles.aggregate(pipeline))

WHO_articles.extend(ProMED_articles)

articles = WHO_articles
'''

# Disease: index dictionary
with open('disease_dict.json', 'r') as disease_fp:
    disease_dict = json.load(disease_fp)

# Country: index dictionary
with open('countries_dict.json', 'r') as countries_fp:
    countries_dict = json.load(countries_fp)

# Preprocess articles and convert to csv for each disease
print("Processing data and creating disease_data.csv")

# Debugging unseen diseases
unseen = []
# disease: last outbreak date
# last_outbreaks = {disease: "date"} ----> {disease: {country: date}} = {"Ebola": {"MY": "2020-04-27", "US": "2020-01-03"}}
last_outbreaks = {}

for article in articles:
    disease = 0
    days_since_last_outbreak = 0
    year_started = 0
    event_days = 0
    country = 0
    n_reports = 0
    outbreak = 0

    # event_days
    expr = re.compile('\d+-\d+-[\dx]+')
    if len(article['reports']) == 0:
        continue
    event_dates_list = expr.findall(article['reports'][0]['event_date'])
    event_dates_list = [date.replace('xx', '01') for date in event_dates_list]
    
    if len(event_dates_list) == 1:
        event_days = 1
    else:
        start_y = int(event_dates_list[0].split('-')[0])
        start_m = int(event_dates_list[0].split('-')[1])
        start_d = int(event_dates_list[0].split('-')[2])
        end_y = int(event_dates_list[1].split('-')[0])
        end_m = int(event_dates_list[1].split('-')[1])
        end_d = int(event_dates_list[1].split('-')[2])

        start_date = date(start_y, start_m, start_d)
        end_date = date(end_y, end_m, end_d)

        event_days = abs(end_date - start_date).days

    # year_started
    year_started = int(event_dates_list[0].split('-')[0])

    # outbreak
    if 'outbreak' in article['main_text'] or 'outbreak' in article['headline']:
        outbreak = 1

    # diseases
    for case in article['reports'][0]['diseases']:
        if case == None:
            continue
        if case in disease_dict.keys():
            disease = disease_dict[case]
        else:
            disease = disease_dict['other']
            if case not in unseen:
                unseen.append(case)

        # country and n_reports
        article_country_count = {}
        for report in article['reports']:
            if report['countries'] == None:
                continue
            for country in report['countries']:
                article_country_count[country] = report['country_count'][country]
                
        # count unique countries and their counts, add to dictionary
        # match with code in countries_dict
        # set country and n_reports to match
        for country_key in article_country_count.keys():
            if country_key in countries_dict.keys():
                country = countries_dict[country_key]
            else:
                country = 0
            n_reports = article_country_count[country_key]

            # last outbreak
            if case not in last_outbreaks.keys():
                days_since_last_outbreak = 0
            else:
                if country_key not in last_outbreaks[case].keys():
                    days_since_last_outbreak = 0
                else:
                    last_y = int(last_outbreaks[case][country_key].split('-')[0])
                    last_m = int(last_outbreaks[case][country_key].split('-')[1])
                    last_d = int(last_outbreaks[case][country_key].split('-')[2])
                    curr_y = int(event_dates_list[0].split('-')[0])
                    curr_m = int(event_dates_list[0].split('-')[1])
                    curr_d = int(event_dates_list[0].split('-')[2])

                    last_date = date(last_y, last_m, last_d)
                    curr_date = date(curr_y, curr_m, curr_d)

                    days_since_last_outbreak = abs(curr_date - last_date).days
            
            if outbreak == 1:
                if case not in last_outbreaks.keys():
                    last_outbreaks[case] = {}
                else:
                    last_outbreaks[case][country_key] = event_dates_list[-1]
                    
            

            with open('disease_data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([disease] + [days_since_last_outbreak] + [year_started] + [event_days] + [country] + [n_reports] + [outbreak])

if len(unseen) != 0:
    print("Unseen diseases, please add to disease_dict.json:", unseen)

with open('last_outbreaks.json', 'w') as ofp:
    json.dump(last_outbreaks, ofp)

print("last_outbreaks.json created")