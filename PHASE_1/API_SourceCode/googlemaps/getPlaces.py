import re
from .googleplacesapi import getGeoData 
import string
from unidecode import unidecode
import os
import json
import pycountry

# THIS IS THE FUNCTION YOU USE
# Pass in the text, and the country(s) relating to it
# Returns a list containing all the location paramaters including City, State, Country, Continent, where aplicable, with duplicates removed
def getPlaces(txt, countries):
    txt0 = "I went to Japan and bought some Colorado hot dogs made by Sydney. I am from the Democratic Republic of Congo, my parents are from Boznia and Herzegovina"
    txt1 = "The case-patient is a 65-year-old male national, living in Doha. He developed cough, palpitations, dizziness, chills and rigor on 9 February, and was admitted to a hospital on the same day. A nasopharyngeal swab was collected on 17 February and tested positive for MERS-CoV by reverse transcriptase polymerase chain reaction (RT-PCR) (UpE and Orf1a genes) at the Department of Laboratory Medicine and Pathology (DLMP) in Hamad Medical Corporation on 17 February. He has underlying comorbidities including diabetes, hypertension, obesity, and coronary artery disease. He is in critical condition and has been isolated in the intensive care unit. The case-patient has a history of close contact with dromedary camels in the 14 days prior to the onset of symptoms."
    txt2 = 'From January 2019 through 17 February 2020, a total of 487 confirmed cases of dengue, with no severe cases or deaths, was reported (Figure 1). The most affected communes were Kourou, on the coastline, with 225 confirmed cases, and Maripasoula, in the south-eastern part of French Guiana with 55 confirmed cases. Except during 2017 and 2018, dengue cases have been reported every year, with the most recent largest outbreak reported in 2013, resulting in 13,240 suspected cases including 6 deaths.'
    txt3 = "WHO has received reports of an outbreak of yellow fever in Batie, Gaoua and Banfora districts in Burkina Faso in the southeast of the country, near the border with Côte d'Ivoire. Four cases including 1 death have been laboratory confirmed by Centre Muraz, Burkina Faso and by the WHO Collaborating Centre for Yellow Fever, the Institut Pasteur, Dakar, Senegal. The fatal case, a boy of 4 years old, came from Bouna region in Côte d'Ivoire."
    txt4 = 'From 1 January through 9 February 2020, 472 laboratory confirmed cases including 70 deaths (case fatality ratio= 14.8%) have been reported in 26 out of 36 Nigerian states and the Federal Capital Territory. Of the 472 confirmed cases, 75% have been reported from three states: Edo (167 cases), Ondo (156 cases) and Ebonyi (30 cases). The other states that have reported cases include : Taraba (25), Bauchi (14), Plateau (13), Kogi (13), Delta (12), Nasarawa (4), Kano (4), Rivers (4), Enugu (4), Borno (3), Kaduna (3), Katsina (3), Benue (2), Adamawa (2), Sokoto (2), Osun (2), Abia (2), Kebbi (2), Gombe (1), Oyo (1), Anambra (1), FCT (1), and Ogun (1).'
    txt5 = "The Department of Health has informed today that there are no new cases of influenza A(H5N1) since the 16th case was confirmed on 3 January. One suspect case remains under investigation."

    txtn = txt.replace(',', '')
    txtn = txtn.replace("Côte d'Ivoire", 'Ivory Coast')
    txtn = unidecode(txtn)
    # print(txtn)
    #print(txt)

    res = re.findall("(([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)|[A-Z][a-z]+[\w])", txtn)
    alt = re.findall("\w*[A-Z]\w*[A-Z]\w*", txtn)
    words = []
    # print("HERE")

    for tup in res:
        if tup[0] == '' or tup[1] == '':
            words.append(tup[0]+tup[1])
        else:
            words.append(tup[0])
    # print(words)
    words = words + alt
    words = list(dict.fromkeys(words))
    ans = removeStopWords(words)  
    # print(ans)
    # print("calling google api")
    result = getGeoData(ans, countries)
    retVal = list(filter(None, result))
    # print(retVal)
    return retVal
    
countries = {
	"Africa": "Africa",
	"Côte d'Ivoir": "Ivory Coast",
	"Côte d’Ivoire": "Ivory Coast",
	"Côte dÎvoire": "Ivory Coast",
    "Côte d'Ivoire": "Ivory Coast",
	"Bolivia": "Bolivia",
	"Middle East": "Middle East",
	"Venezuela": "Venezuela",
	"Americas": "Americas",
	"Lao People's Democratic Republic": "Laos",
	"Toronto": "Toronto",
	"Tanzania": "Tanzania",
	"Micronesia": "Micronesia",
	"Gaza": "Gaza",
	"Europe": "Europe",
	"Kosovo": "Kosovo",
	"Iran": "Iran",
	"Zaire": "Zaire",
	"Taiwan": "Taiwan",
	"Asia": "Asia",
	"Cape Verde": "Cape Verde", 
	"Argentine": "Argentina",
	"Democratic People's Republic of Korea": "North Korea"
}
def get_country(headline):
	headline = headline.lower()
	for country in pycountry.countries:
		if country.name.lower() in headline:
			return country.name
		for key in countries:
			if key.lower() in headline:
				return countries[key]
	return ""

def removeStopWords(words):
    # TODO Remove diseases from the list
    stopwords = ['The', 'He', 'She', 'They' 
                 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
                 'Monday', 'Teusday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Zero',
                 'Department', 'Laboratory Medicine', 'Pathology', 'Collaborating Centre',
                 'Democratic Republic', 'Medecins', 'Ministry', 'Health',
                 'Figure', 'WHO', 'Puumala']

    curPath = os.path.dirname(__file__)
    parPath = os.path.abspath(os.path.join(curPath, os.pardir))
    # newPath = os.path.relpath('../disease/disease_list.json', curPath)
    newPath = os.path.join(parPath, 'disease', 'disease_list.json')

    with open(newPath, 'r') as f:
        data = json.load(f)
        for dis in data:
            stopwords = stopwords + dis['WHO']
    #print(stopwords)


    ans = [word for word in words if word not in stopwords]
   

    #print(ans)
    #regex = re.compile('\w*[A-Z]\w*[A-Z]\w*')
    #ans1 = [word for word in ans if not regex.match(word)]


    return ans

# getPlaces('', ['Qatar'])