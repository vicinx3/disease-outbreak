export const disease_list = require('./disease_list.json');
disease_list.unshift('all diseases');

export const disease_conversion = require('./disease_conversion.json');
disease_conversion['all diseases'] = 'All diseases';

export const country_list = require('./country_codes.json');
country_list.unshift('all countries');

export const country_conversion = require('./country_code_conversion.json');
country_conversion['all countries'] = 'All countries';

export const covid_country_list = require('./covid_countries.json');
covid_country_list.unshift('all countries');