import json
import ndjson
import pprint

with open('country_list.json', 'r') as fp:
    country_list = json.load(fp)

countries_dict = {}
countries_dict['other'] = 0
i = 1
while i <= len(country_list):
    countries_dict[country_list[i - 1]] = i
    i += 1

with open('countries_dict.json', 'w') as fp:
    json.dump(countries_dict, fp)

with open('disease_list.json', 'r') as fp:
    disease_list = json.load(fp)

disease_dict = {}
disease_dict['other'] = 0
i = 1
while i <= len(disease_list):
    disease_dict[disease_list[i - 1]] = i
    i += 1

with open('disease_dict.json', 'w') as fp:
    json.dump(disease_dict, fp)
