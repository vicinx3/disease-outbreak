from sys import argv
import os 
from json import load
from glob import glob 
from PHASE_1.API_SourceCode.dateparse.event_date import get_event_date

dirname = os.path.dirname(__file__)

def get_json(prefix):
	path = glob(os.path.join(dirname, 'jsons', prefix + '*'))[0]
	with open(path, 'r') as f: 
		data = load(f)
	return data

if __name__ == "__main__":
	if len(argv) == 2:
		print(get_json(argv[1]))

def test_1996_02_05():
	data = get_json('1996-02-05')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1995-01-xx xx:xx:xx to 1995-11-xx xx:xx:xx'

def test_1996_02_08():
	data = get_json('1996-02-08')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1996-02-08 xx:xx:xx'

def test_1996_05_28():
	data = get_json('1996-05-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1996-05-28 xx:xx:xx'

def test_1996_08_02():
	data = get_json('1996-08-02')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1996-05-xx xx:xx:xx'

def test_1997_02_28():
	data = get_json('1997-02-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1997-01-xx xx:xx:xx to 1997-02-15 xx:xx:xx'

def test_1997_02_28():
	data = get_json('1997-02-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1997-01-xx xx:xx:xx to 1997-02-15 xx:xx:xx'

def test_1997_07_31():
	data = get_json('1997-07-31')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1997-03-xx xx:xx:xx to 1997-05-xx xx:xx:xx'

def test_1998_01_09():
	data = get_json('1998-01-09')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1998-01-03 xx:xx:xx'

def test_1998_08_23():
	data = get_json('1998-10-23')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1998-10-xx xx:xx:xx'

def test_1999_03_26():
	data = get_json('1999-03-26')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1999-03-19 xx:xx:xx'

def test_1999_11_19():
	data = get_json('1999-11-19')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '1999-07-30 xx:xx:xx'

def test_2000_01_28():
	data = get_json('2000-01-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2000-01-12 xx:xx:xx'

def test_2000_09_18():
	data = get_json('2000-09-18')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2000-09-17 xx:xx:xx'

def test_2001_01_09():
	data = get_json('2001-01-09')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2000-12-19 xx:xx:xx to 2001-01-09 xx:xx:xx'

def test_2001_02_28():
	data = get_json('2001-02-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-02-28 xx:xx:xx'

def test_2001_03_19():
	data = get_json('2001-03-19')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-01-01 xx:xx:xx to 2001-03-16 xx:xx:xx'

def test_2001_04_09():
	data = get_json('2001-04-09')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-04-09 xx:xx:xx'

def test_2001_05_31():
	data = get_json('2001-05-31')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-03-23 xx:xx:xx to 2001-03-24 xx:xx:xx'

def test_2001_06_05():
	data = get_json('2001-06-05')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-04-26 xx:xx:xx to 2001-05-10 xx:xx:xx'

def test_2001_07_26():
	data = get_json('2001-07-26')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-07-25 xx:xx:xx'

def test_2001_08_15():
	data = get_json('2001-08-15')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-08-12 xx:xx:xx'

def test_2001_08_15():
	data = get_json('2001-08-15')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-08-12 xx:xx:xx'

def test_2001_09_18():
	data = get_json('2001-09-18')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-09-17 xx:xx:xx'

def test_2001_10_30():
	data = get_json('2001-10-30')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-10-30 xx:xx:xx'

def test_2001_11_12():
	data = get_json('2001-11-12')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-11-12 xx:xx:xx'

def test_2001_11_12():
	data = get_json('2001-11-12')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-11-08 xx:xx:xx'

def test_2001_12_12():
	data = get_json('2001-12-12')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2001-12-12 xx:xx:xx'

def test_2002_02_20():
	data = get_json('2002-02-20')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2002-02-04 xx:xx:xx to 2002-02-19 xx:xx:xx'

def test_2003_07_28():
	data = get_json('2003-07-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2003-07-28 xx:xx:xx'

# This is HARD, requires understanding context around sentenecs!!
def test_2004_04_23():
	data = get_json('2004-04-23')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2004-04-23 xx:xx:xx'

def test_2005_03_31():
	data = get_json('2005-03-31')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2005-03-21 xx:xx:xx to 2005-03-27 xx:xx:xx'

def test_2006_05_10():
	data = get_json('2006-05-10')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2006-02-19 xx:xx:xx to 2006-05-08 xx:xx:xx'

def test_2007_09_14():
	data = get_json('2007-09-14')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2007-07-29 xx:xx:xx to 2007-09-12 xx:xx:xx'

def test_2008_03_07():
	data = get_json('2008-03-07')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2008-03-07 xx:xx:xx'
	
def test_2009_10_01():
	data = get_json('2009-10-01')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2009-07-27 xx:xx:xx to 2009-09-08 xx:xx:xx'

def test_2010_03_12():
	data = get_json('2010-03-12')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2010-02-27 xx:xx:xx to 2010-03-09 xx:xx:xx'

def test_2011_04_11():
	data = get_json('2011-04-11')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2011-03-01 xx:xx:xx'

def test_2012_08_10():
	data = get_json('2012-08-10')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2012-08-04 xx:xx:xx'

def test_2013_12_31():
	data = get_json('2013-12-31')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2013-11-25 xx:xx:xx to 2013-12-26 xx:xx:xx'

def test_2014_05_24():
	data = get_json('2014-05-24')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2014-05-23 xx:xx:xx'

def test_2015_03_17():
	data = get_json('2015-03-17')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2015-02-24 xx:xx:xx'

def test_2016_08_09():
	data = get_json('2016-08-09')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2016-05-28 xx:xx:xx to 2016-06-30 xx:xx:xx'

def test_2017_11_15():
	data = get_json('2017-11-15')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2017-08-01 xx:xx:xx to 2017-11-15 xx:xx:xx'

def test_2018_02_27():
	data = get_json('2018-02-27')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2018-01-04 xx:xx:xx to 2018-02-03 xx:xx:xx'

def test_2019_01_08():
	data = get_json('2019-01-08')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2018-10-06 xx:xx:xx to 2018-10-07 xx:xx:xx'

def test_2019_02_11():
	data = get_json('2019-02-11')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2018-12-xx xx:xx:xx to 2019-01-xx xx:xx:xx'

def test_2019_04_04():
	data = get_json('2019-04-04')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-03-13 xx:xx:xx to 2019-04-02 xx:xx:xx'

def test_2019_06_06():
	data = get_json('2019-06-06')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-04-xx xx:xx:xx to 2019-06-04 xx:xx:xx'

def test_2019_08_01():
	data = get_json('2019-08-01')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-07-11 xx:xx:xx to 2019-08-01 xx:xx:xx'

def test_2019_08_01():
	data = get_json('2019-08-01')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-07-11 xx:xx:xx to 2019-08-01 xx:xx:xx'

def test_2019_11_28():
	data = get_json('2019-11-28')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-11-04 xx:xx:xx to 2019-11-24 xx:xx:xx'

def test_2019_12_18():
	data = get_json('2019-12-18')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-11-01 xx:xx:xx to 2019-11-30 xx:xx:xx'

def test_2020_01_02():
	data = get_json('2020-01-02')
	result = get_event_date(data['main_text'], data['date_of_publication'])
	assert result == '2019-12-11 xx:xx:xx to 2019-12-31 xx:xx:xx'

	