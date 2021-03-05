# Database interactions

from pymongo import MongoClient
from datetime import datetime
from calendar import monthrange
from pycountry_convert import country_name_to_country_alpha2, country_alpha2_to_country_name
from pprint import pprint
import json

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb+srv://codeonavirus:codeonavirus@codeonavirus-etwjy.mongodb.net/test?retryWrites=true&w=majority')
db = client.app_database
articles = db.articles

def db_drop():
    articles.drop()

def db_insert(source, article, date_format=r'%Y-%m-%d %H:%M:%S'):
    # Convert date of publication to datetime 
    date = datetime.strptime(article['date_of_publication'], date_format)
    article['date_of_publication'] = date 
    article['source'] = source 

    # Convert country to country code
    for i, report in enumerate(article['reports']):
        codes = {}
        for j, location in enumerate(report['locations']):
            if location['country'] == None: 
                continue
            code = convert_country(location['country'])
            if code in codes:
                codes[code] += 1
            else: 
                codes[code] = 1
        article['reports'][i]['countries'] = list(codes.keys())
        article['reports'][i]['country_count'] = codes

        for j, disease in enumerate(report['diseases']):
            article['reports'][i]['diseases'][j] = convert_disease(disease)

    articles.insert_one(article)

def db_delete_GIM():
    query = {"source": "GIM"}
    n = articles.delete_many(query)
    print(n.deleted_count, "documents deleted.")

def convert_disease(disease):
    preset = {
        'mers': 'mers-cov',
        'enterotoxin': 'staphylococcal enterotoxin b',
        'rotavirus': 'rotavirus infection',
        'e.coli': 'ehec (e.coli)',
        'e. coli': 'ehec (e.coli)',
        'pneumococcus': 'pneumococcus pneumonia',
        'marburg virus': 'marburg virus disease',
        'hiv': 'hiv/aids',
        'aids': 'hiv/aids',
        'norovirus': 'norovirus infection',
        'a/h1n1': 'influenza a/h1n1',
        'a/h3n2': 'influenza a/h3n2',
        'a/h5n1': 'influenza a/h5n1',
        'a/h9n2': 'influenza a/h9n2',
        'ebola': 'ebola haemorrhagic fever',
        'crimean-congo hemorrhagic fever': 'crimean-congo haemorrhagic fever',
        'vaccinia': 'vaccinia and cowpox',
        'cowpox': 'vaccinia and cowpox',
        'pneumococcal pneumonia': 'pneumococcus pneumonia',
        'staphylococcal': 'staphylococcal enterotoxin b',
        'enterovirus 71': 'enterovirus 71 infection',
        'thypoid fever': 'typhoid fever'
    }
    if disease in preset:
        return preset[disease]
    return disease

def convert_country(country):
    # Possible hard-coded countries here
    preset = {
        'The Gambia': 'GM',
        'Kosovo': 'XK', 
        'Myanmar (Burma)': 'MM',
        'Sint Maarten': 'SX',
        'U.S. Virgin Islands': 'VI',
        'Caribbean Netherlands': 'BQ',
        'The Bahamas': 'BS',
        'Serbia And Montenegro': 'CS', 
        'Macao S.A.R., China': 'MO',
        'Hong Kong S.A.R., China': 'HK',
        'Netherlands Antilles': 'ANT',
        'Palestinian Territory': 'PS',
        'Congo (Kinshasa)': 'CD',
        'Congo (Brazzaville)': 'CG',
        'Saint Helena': 'SH',
        'Reunion': 'RE',
        'St Lucia': 'LC',
        'Vatican': 'VA',
        '00120, Vatican City': 'VA',
        '6798, Christmas Island': 'CX',
        'FIQQ 1ZZ, Falkland Islands (Islas Malvinas)': 'FK',
        'TKCA 1ZZ, Turks and Caicos Islands': 'TC'
    }
    
    if country in preset:
        return preset[country]

    try: 
        return country_name_to_country_alpha2(country)

    # If any countries fall through filters
    except Exception: 
        f = open('debug.txt', 'a+')
        f.write('Failed convert_country: ' + country + '\n')
        f.close()
        return country

def convert_code(code):
    preset = {
        'TW': 'Taiwan',
        'XK': 'Kosovo',
        'LA': 'Laos',
        'SY': 'Syria',
        'MD': 'Moldova',
        'BO': 'Bolivia',
        'VE': 'Venezuela',
        'KP': 'North Korea',
        'FM': 'Federated States of Micronesia',
        'FK': 'Falkland Islands',
        'KR': 'South Korea',
        'PS': 'Palestine',
        'CD': 'Democratic Republic of the Congo',
        'BQ': 'Bonaire, Sint Eustatius and Saba',
        'BN': 'Brunei',
        'TZ': 'Tanzania',
        'VI': 'U.S. Virgin Islands',
        'VA': 'Vatican City',
        'IR': 'Iran',
        'VG': 'British Virgin Islands'
    }

    if code in preset: 
        return preset[code]
    return country_alpha2_to_country_name(code)

def prettify_disease(disease):
    preset = {
        'crimean-congo haemorrhagic fever': 'Crimean-Congo haemorrhagic fever',
        'COVID-19': 'COVID-19',
        'ehec (e.coli)':  'EHEC (E.coli)',
        'hepatitis a': 'Hepatitis A',
        'hepatitis b': 'Hepatitis B',
        'hepatitis c': 'Hepatitis C',
        'hepatitis d': 'Hepatitis D',
        'hepatitis e': 'Hepatitis E',
        'hiv/aids': 'HIV/AIDS',
        'influenza a/h1n1': 'Influenza A/H1N1',
        'influenza a/h1n2': 'Influenza A/H1N2',
        'influenza a/h3n2': 'Influenza A/H3N2',
        'influenza a/h5n1': 'Influenza A/H5N1',
        'influenza a/h5n6': 'Influenza A/H5N6',
        'influenza a/h7n2': 'Influenza A/H7N2',
        'influenza a/h7n4': 'Influenza A/H7N4',
        'influenza a/h7n9': 'Influenza A/H7N9',
        'influenza a/h9n2': 'Influenza A/H9N2',
        'mers-cov': 'MERS-CoV',
        'sars': 'SARS',
        'staphylococcal enterotoxin b': 'Staphylococcal enterotoxin B',
        'vaccinia and cowpox': 'Vaccinia and Cowpox',
        'west nile virus': 'West Nile virus'
    }
    if disease in preset:
        return preset[disease]
    else:
        return disease.capitalize()

def check_new_article(url):
    pipeline = [
        {'match': {'url': url}}
    ]

    result = list(articles.aggregate(pipeline))
    if len(result) > 1: 
        print("Something went wrong!!!")
    return len(result) == 1

def add_match_source(pipeline, source, i=0):
    if source != '':
        match = {'$match': {'source': source}}
        pipeline.insert(i, match)

def add_match_country(pipeline, country, i=0):
    if country != '':
        match = {'$match': {'reports.countries': {'$in': [country]}}} 
        pipeline.insert(i, match)

def add_match_disease(pipeline, disease, i=0):
    if disease != '':
        match = {'$match': {'reports.diseases': {'$in': [disease]}}} 
        pipeline.insert(i, match)

def match_year_month(year, month=0):
    start_month = 1 if month == 0 else month 
    start_date = datetime(year, start_month, 1)

    end_month = 12 if month == 0 else month 
    end_day = monthrange(year, end_month)[1]
    end_date = datetime(year, end_month, end_day, 23, 59, 59)

    return {'$match': {'date_of_publication': {'$gte': start_date, '$lte': end_date}}}

def get_country_list(sort=False, name=False):
    pipeline = [
        {'$unwind': '$reports'},
        {'$unwind': '$reports.countries'},
        {'$group': {'_id': '$reports.countries'}}
    ]

    result = [element['_id'] for element in articles.aggregate(pipeline)]
    if sort:
        if not name: 
            result.sort()
        else: 
            result.sort(key=convert_code)
    return result

def get_country_dict():
    return { code: convert_code(code) for code in get_country_list()}

def get_disease_list(sort=False, prettify=False):
    pipeline = [
        {'$unwind': '$reports'},
        {'$unwind': '$reports.diseases'},
        {'$group': {'_id': '$reports.diseases'}}
    ]

    result = [element['_id'] for element in articles.aggregate(pipeline)]
    if sort:
        result.sort()
    if prettify:
        result = [prettify_disease(disease) for disease in result]
    return result

def get_disease_dict():
    return {disease: prettify_disease(disease) for disease in get_disease_list()}

def get_article_summary(source, year, month, country, disease, sort=True):
    pipeline = [
        match_year_month(year, month),
        {'$project': {'_id': 0, 'url': 1, 'headline': 1, 'date_of_publication': 1, 'source': 1, 'date': {'$dateToString': {'format': '%d/%m/%Y %H:%M:%S', 'date': '$date_of_publication'}}}}
    ]
    add_match_source(pipeline, source)
    add_match_country(pipeline, country)
    add_match_disease(pipeline, disease)

    result = list(articles.aggregate(pipeline))
    if sort: 
        result.sort(key=lambda x: x['date_of_publication'])
    return result 

def get_article(url):
    pipeline = [
        {'$match': {'url': url}},
        {'$project': {'_id': 0, 'url': 1, 'date_of_publication': 1, 'headline': 1, 'main_text': 1, 'date': {'$dateToString': {'format': '%d/%m/%Y %H:%M:%S', 'date': '$date_of_publication'}}}}
    ]

    result = list(articles.aggregate(pipeline))
    return result[0]

def get_num_reports_by_country(source, year, month, country, disease, merge=False, maxResults=0):
    pipeline = [
        match_year_month(year, month),
        {'$unwind': '$reports'},
        {'$unwind': '$reports.countries'},
        {'$group': {'_id': '$reports.countries', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'category': '$_id', 'value': 1}}
    ]
    add_match_source(pipeline, source)
    add_match_country(pipeline, country)
    add_match_disease(pipeline, disease)

    result = list(articles.aggregate(pipeline))
    if maxResults > 0:
        result.sort(key=lambda x: x['value'], reverse=True)
        other = sum([pair['value'] for pair in result[maxResults:]])
        result = result[:maxResults] + [{'category': 'remaining', 'value': other}]
    if merge: 
        new_result = {}
        for pair in result:
            new_result[pair['category']] = pair['value']
        return new_result
    else: 
        return result 

def get_num_reports_by_disease(source, year, month, country, disease, maxResults=0, prettify=False):
    pipeline = [
        match_year_month(year, month),
        {'$unwind': '$reports'},
        {'$unwind': '$reports.diseases'},
        {'$group': {'_id': '$reports.diseases', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'category': '$_id', 'value': 1}}
    ]
    add_match_source(pipeline, source)
    add_match_country(pipeline, country)
    add_match_disease(pipeline, disease)

    result = list(articles.aggregate(pipeline))
    result.sort(key=lambda x: x['value'], reverse=True)
    if maxResults > 0 and len(result) > maxResults:
        other = sum([pair['value'] for pair in result[maxResults:]])
        result = result[:maxResults] + [{'category': 'remaining', 'value': other}]
    if prettify: 
        result = [{'category': prettify_disease(pair['category']), 'value': pair['value']} for pair in result]
    return result 

def get_num_total_reports():
    pipeline = [
        {'$count': 'total'},
    ]
    result = list(articles.aggregate(pipeline))
    return result[0]

def get_num_reports_by_year(source, country='', disease=''):
    # country is a country code 
    pipeline = [
        {'$unwind': '$reports'},
        {'$project': {'article_year': {'$year': '$date_of_publication'}}},
        {'$group': {'_id': '$article_year', 'value': {'$sum': 1}}},
        {'$project': {'_id': 0, 'date': '$_id', 'value': 1}}
    ]
    add_match_country(pipeline, country, 1)
    add_match_disease(pipeline, disease, 1)
    add_match_source(pipeline, source)

    # if country != '': 
    #     match = {'$match': {'reports.countries': {'$in': [country]}}} 
    #     pipeline.insert(1, match)

    # if disease != '':
    #     match = {'$match': {'reports.diseases': {'$in': [disease]}}} 
    #     pipeline.insert(1, match)

    result = list(articles.aggregate(pipeline))[:]
    
    # Fill intermediate values 
    for i in range(1996, 2021):
        if i not in [pair['date'] for pair in result]:
            result.append({
                'date': i,
                'value': 0
            })
    result.sort(key=lambda x: x['date'])
    return result

def download(source=''):
    with open('results_mongo.json', 'w') as f:
        pipeline = [
            {'$project': {'_id': 0, 'headline': 1, 'main_text': 1, 'reports': 1}}
        ]

        if source != '':
            pipeline.insert(0, {'$match': {'source': source}})

        result = list(articles.aggregate(pipeline))
        json.dump(result, f)