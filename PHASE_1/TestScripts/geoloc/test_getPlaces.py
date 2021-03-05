from json import load
from PHASE_1.API_SourceCode.googlemaps.getPlaces import getPlaces
import pytest
import os
from glob import glob
import collections

dirname = os.path.dirname(__file__)

def get_json(prefix):
	path = glob(os.path.join(dirname, 'Updated JSON_s', prefix + '*'))[0]
	with open(path, 'r') as f: 
		data = load(f)
	return data

if __name__ == "__main__":
	if len(argv) == 2:
		print(get_json(argv[1]))

def equal_ignore_order(a, b):
    """ Use only when elements are neither hashable nor sortable! """
    unmatched = list(b)
    for element in a:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return not unmatched

def test_1996_02_05():
	data = get_json('1996-02-05')
	result = getPlaces(data['main_text'], ['Bosnia and Herzegovina'])
	print(result)
	assert result == [{'country': 'Bosnia and Herzegovina', 'continent': 'Europe'}]

def test_1996_02_08():
	data = get_json('1996-02-08')
	result = getPlaces(data['main_text'], ['Iran'])
	print(result)
	assert result == [{'city': 'Tehran', 'state': 'Tehran Province', 'country': 'Iran', 'continent': 'Asia'}]

def test_1997_07_31():
	data = get_json('1997-07-31')
	result = getPlaces(data['main_text'], ['Democratic Republic of the Congo'])
	print(result)
	testVal = [{'city': 'Katako-Kombe', 'state': 'Kasai Oriental', 'country': 'Democratic Republic of the Congo', 'continent': 'Africa'}, {'country': 'Democratic Republic of the Congo', 'continent': 'Africa'}, {'state': 'Kasai Oriental', 'country': 'Democratic Republic of the Congo', 'continent': 'Africa'}, {'city': 'Lubumbashi', 'state': 'Katanga', 'country': 'Democratic Republic of the Congo', 'continent': 'Africa'}, {'city': 'Lodja', 'state': 'Kasai Oriental', 'country': 'Democratic Republic of the Congo', 'continent': 'Africa'}, {'city': 'Kinshasa', 'state': 'Kinshasa', 'country': 'Democratic Republic of the Congo', 'continent': 'Africa'}]
	assert equal_ignore_order(result, testVal) == True

def test_1998_01_09():
	data = get_json('1998-01-09')
	result = getPlaces(data['main_text'], ['Hong Kong'])
	print(result)
	assert result == [{'state': 'Hong Kong Island', 'country': 'Hong Kong', 'continent': 'Asia'}]

def test_1999_03_26():
	data = get_json('1999-03-26')
	result = getPlaces(data['main_text'], ['Sudan'])
	print(result)
	assert result == [{'country': 'Sudan', 'continent': 'Africa'}]

def test_2002_02_20():
	data = get_json('2002-02-20')
	result = getPlaces(data['main_text'], ['India'])
	print(result)
	testVal = [{'city': 'Shimla', 'state': 'Himachal Pradesh', 'country': 'India', 'continent': 'Asia'}, {'city': 'Hatkoti', 'state': 'Himachal Pradesh', 'country': 'India', 'continent': 'Asia'}, {'city': 'Ahmedabad', 'state': 'Gujarat', 'country': 'India', 'continent': 'Asia'}, {'city': 'New Delhi', 'state': 'Delhi', 'country': 'India', 'continent': 'Asia'}, {'state': 'Himachal Pradesh', 'country': 'India', 'continent': 'Asia'}, {'city': 'Bethesda', 'state': 'Maryland', 'country': 'United States', 'continent': 'North America'}, {'city': 'Jodhpur', 'state': 'Rajasthan', 'country': 'India', 'continent': 'Asia'}, {'country': 'India', 'continent': 'Asia'}]
	assert equal_ignore_order(result, testVal) == True

def test_2015_03_17():
	data = get_json('2015-03-17')
	result = getPlaces(data['main_text'], ['Uganda'])
	print(result)
	testVal = [{'country': 'Uganda', 'continent': 'Africa'}, {'city': 'Kampala', 'state': 'Central Region', 'country': 'Uganda', 'continent': 'Africa'}]
	assert equal_ignore_order(result, testVal) == True

""" Quite Long, But works
def test_2020_03_04():
	data = get_json('2020-03-04')
	result = getPlaces(data['main_text'], ['Central African Republic'])
	print(result)
	testVal = [{'city': 'Bambari', 'state': 'Ouaka', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Mingala', 'state': 'Basse-Kotto', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Congo', 'state': 'Basse-Kotto', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Alindao', 'state': 'Basse-Kotto', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Paris', 'state': 'Île-de-France', 'country': 'France', 'continent': 'Europe'}, {'country': 'Chad', 'continent': 'Africa'}, {'country': 'Cameroon', 'continent': 'Africa'}, {'city': 'Bangui', 'state': 'Bangui', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Bimbo', 'state': "Ombella-M'Poko", 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Ouango', 'state': 'Mbomou', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Kouango', 'state': 'Ouaka', 'country': 'Central African Republic', 'continent': 'Africa'}, {'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Gambo', 'state': 'Mbomou', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Abba', 'state': 'Nana-Mambéré', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Gribizi', 'state': 'Nana-Grebizi', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Grimari', 'state': 'Ouaka', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Washington', 'state': 'District of Columbia', 'country': 'United States', 'continent': 'North America'}, {'city': 'Nana', 'state': 'Nana-Grebizi', 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Bossembélé', 'state': "Ombella-M'Poko", 'country': 'Central African Republic', 'continent': 'Africa'}, {'city': 'Boguila', 'state': 'Ouham-Pendé', 'country': 'Central African Republic', 'continent': 'Africa'}]
	assert equal_ignore_order(result, testVal) == True
"""

def test_1996_03_01():
	data = get_json('1996-03-01')
	result = getPlaces(data['main_text'], ['Nigeria'])
	print(result)
	testVal = [{'city': 'Abuja', 'state': 'Federal Capital Territory', 'country': 'Nigeria', 'continent': 'Africa'}, {'state': 'Kano', 'country': 'Nigeria', 'continent': 'Africa'}, {'city': 'Kano', 'state': 'Kano', 'country': 'Nigeria', 'continent': 'Africa'}, {'state': 'Oyo', 'country': 'Nigeria', 'continent': 'Africa'}]
	assert equal_ignore_order(result, testVal) == True

def test_1996_08_12():
	data = get_json('1996-08-12')
	result = getPlaces(data['main_text'], ['Ghana'])
	print(result)
	assert result == [{'country': 'Ghana', 'continent': 'Africa'}]

def test_1997_03_11():
	data = get_json('1997-03-11')
	result = getPlaces(data['main_text'], ['Bolivia'])
	print(result)
	testVal = [{'state': 'La Paz Department', 'country': 'Bolivia', 'continent': 'South America'}, {'state': 'Beni Department', 'country': 'Bolivia', 'continent': 'South America'}, {'city': 'La Paz', 'state': 'La Paz Department', 'country': 'Bolivia', 'continent': 'South America'}, {'state': 'Cochabamba Department', 'country': 'Bolivia', 'continent': 'South America'}, {'state': 'Santa Cruz Department', 'country': 'Bolivia', 'continent': 'South America'}]
	assert equal_ignore_order(result, testVal) == True