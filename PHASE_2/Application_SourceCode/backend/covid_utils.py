import requests
import datetime
from db import convert_code
from pycountry_convert import country_name_to_country_alpha2
from pprint import pprint
import json

url = r'https://pomber.github.io/covid19/timeseries.json'
response = requests.get(url)
if response.status_code != 200:
    print("Failed to connect to pomber")

def convert_country(country):
    preset = {
        'Congo (Brazzaville)': 'CG',
        'Congo (Kinshasa)': 'CD',
        'Cote d\'Ivoire': 'CI',
        'Holy See': 'VA',
        'Korea, South': 'KR',
        'Taiwan*': 'TW',
        'US': 'US',
        'West Bank and Gaza': 'PS',
        'Kosovo': 'XK',
        'Burma': 'MM',
    }
    if country in preset: 
        return preset[country]
    try: 
        return country_name_to_country_alpha2(country)    
    except Exception: 
        return False 

result = response.json()
content = {} 
for country in result:
    code = convert_country(country)
    if code:
        content[code] = result[country]

def get_date(index): 
    date_str = content['AU'][index]['date']
    return datetime.datetime.strptime(date_str, r'%Y-%m-%d')

first_date = get_date(0)
last_date = get_date(-1)

def get_last_day():
    delta = last_date - first_date
    return delta.days

total = []
for i in range(0, get_last_day() + 1): 
    total.append({
        'confirmed': 0,
        'recovered': 0,
        'deaths': 0
    })

    for country in content: 
        for category in ['confirmed', 'recovered', 'deaths']:
            total[i][category] += content[country][i][category]

######################
# Functions 
######################

def get_codes():
    return list(content.keys())

def get_countries():
    result = {}
    for code in content: 
        result[code] = convert_code(code)
    return result

def get_slider_marks():
    marks = []
    template = r'%d %b'
    
    marks.append({'value': 0, 'label': first_date.strftime(template)})
    marks.append({'value': get_last_day(), 'label': last_date.strftime(template)})


    for i in range(0, get_last_day() - 5, 14):
        current_date = first_date + datetime.timedelta(days=i)
        marks.append({'value': i, 'label': current_date.strftime(template)})

    return marks

def get_cases_by_country_and_category(date, category, daily):
    result = {}
    for country in content: 
        if daily: 
            delta = content[country][date][category]
            if date > 0: 
                delta -= content[country][date - 1][category]
            result[country] = delta 
        else: 
            result[country] = content[country][date][category]

    return result


def get_cases_by_country(date, prettify=False):
    def calc_mortality(deaths, recovered): 
        total = deaths + recovered
        return round(deaths * 100 / total, 2) if total > 0 else 0

    result = []
    for country in content:
        current = content[country][date]
        confirmed = current['confirmed']
        recovered = current['recovered']
        deaths = current['deaths']
        mortality = calc_mortality(deaths, recovered)

        result.append({
            'country': convert_code(country),
            'confirmed': confirmed,
            'recovered': recovered,
            'deaths': deaths, 
            'mortality': mortality 
        })

    result.insert(0, {
        'country': 'All countries',
        'confirmed': total[date]['confirmed'], 
        'recovered': total[date]['recovered'],
        'deaths': total[date]['deaths'],
        'mortality': calc_mortality(total[date]['deaths'], total[date]['recovered']) 
    })
    
    return result

def get_cases_by_day(daily):
    result = {}
    for category in ['confirmed', 'recovered', 'deaths']: 
        temp = []
        for i in range(0, get_last_day() + 1):
            current_date = first_date + datetime.timedelta(days=i)
            if daily: 
                value = total[i][category]
                if i > 0:
                    value -= total[i-1][category]
            else:
                value = total[i][category]
            temp.append({
                'date': current_date.strftime(r'%Y-%m-%d'),
                'value': value
            })
        result[category] = temp 

    return result


def get_comparator_graph_data(country):
    standard = {}
    for category in ['confirmed', 'recovered', 'deaths']:
        standard[category] = []
        for i in range(0, get_last_day() + 1):
            value = total[i][category] if country == '' else content[country][i][category]
            standard[category].append({
                'date': i,
                'value': value
            })

    trajectory = []
    for i in range(0, get_last_day() + 1):

        if country == '':
            get = lambda x: total[x]['confirmed']
        else: 
            get = lambda x: content[country][x]['confirmed']   

        total_cases = get(i)

        def daily_increase(j):
            return get(j) - get(j-1) if j > 0 else get(j)

        j = i
        new_cases = 0
        while (j >= 0 and i - j < 7):
            new_cases += daily_increase(j)
            j -= 1
        new_cases = round(new_cases / (i - j))
        if new_cases > 0:
            trajectory.append({
                'total': total_cases, 
                'new': new_cases
            })
    
    return {'standard': standard, 'trajectory': trajectory}