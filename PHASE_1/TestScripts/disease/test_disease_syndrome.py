from sys import argv
import os 
from json import load
from glob import glob 
from PHASE_1.API_SourceCode.disease.diseaseExtractor import diseaseExtractor
from PHASE_1.API_SourceCode.disease.syndromeExtractor import syndromeExtractor

dirname = os.path.dirname(__file__)

def get_json(prefix):
	path = glob(os.path.join(dirname, 'jsons', prefix + '*'))[0]
	with open(path, 'r') as f: 
		data = load(f)
	return data

if __name__ == "__main__":
	if len(argv) == 2:
		print(get_json(argv[1]))


def testAnthrax():
	data = get_json('2001-10-31')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['anthrax cutaneous', "anthrax gastrointestinous", "anthrax inhalation"]

def testBotulism():
	data = get_json('2006-10-11')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['botulism']

def testChikungunya():
	data = get_json('2015-09-14')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['chikungunya']

def testCholera():
	data = get_json('1996-01-22')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['cholera']

def testDengue():
	data = get_json('2015-11-12')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['dengue']

def testDiphteria():
	data = get_json('2017-12-22')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['diphteria']

def testEbola():
	data = get_json('2015-05-13')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['ebola haemorrhagic fever']

def testEcoli():
	data = get_json('2000-05-30')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['ehec (e.coli)']

def testEnterovirus():
	data = get_json('2014-09-17')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['enterovirus 71 infection']

def testH5N6():
	data = get_json('2016-01-26')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['influenza a/h5n6']

def testHantavirus():
	data = get_json('2019-01-23')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['hantavirus']

def testHepatiitsE():
	data = get_json('2018-01-15')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['hepatitis e']

def testHIV():
	data = get_json('2019-07-03')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['hiv/aids']

def testLassaFever():
	data = get_json('2016-01-27')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['lassa fever']

def testMalaria():
	data = get_json('2007-02-09')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['malaria']

def testMERS():
	data = get_json('2015-10-25')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['mers-cov']

def testNipahvirus():
	data = get_json('2018-08-07')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['nipah virus']

def testPertusis():
	data = get_json('2003-01-08')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['pertussis']

def testPneumonia():
	data = get_json('2020-01-05')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['pneumococcus pneumonia']

def testPolio():
	data = get_json('2019-09-24')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['poliomyelitis']

def testRiftValley():
	data = get_json('2019-11-14')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['rift valley fever']

def testSalmonella():
	data = get_json('2016-04-28')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['salmonellosis']

def testSARS():
	data = get_json('2004-04-29')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['sars']

def testShigella():
	data = get_json('2004-07-14')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['shigellosis']

def testStaphylococcalEnterotoxinB():
	data = get_json('2000-07-10')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['staphylococcal enterotoxin b']

def testTyphoid():
	data = get_json('2015-03-17')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['thypoid fever']

def testTuberculosis():
	data = get_json('2007-05-30')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['tuberculosis']

def testTularemia():
	data = get_json('2002-01-25')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['tularemia']

def testWestNileVirus():
	data = get_json('2015-09-17')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['west nile virus']

def testYellowFever():
	data = get_json('2019-12-26')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['yellow fever']

def testZika():
	data = get_json('2016-01-21')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['zika']

def testLegionaires():
	data = get_json('2014-11-13')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['legionares']

def testListeriosis():
	data = get_json('2019-09-16')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['listeriosis']

def testMonkeypox():
	data = get_json('2019-05-16')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['monkeypox']

def testCOVID19():
	data = get_json('2020-01-14')
	result = diseaseExtractor(data['main_text'], data['headline'], data['date_of_publication'])
	assert result == ['COVID-19']