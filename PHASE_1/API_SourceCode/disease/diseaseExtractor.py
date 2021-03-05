import json
import os

dirname = os.path.dirname(__file__)
f = open(os.path.join(dirname, 'disease_list.json'), 'r')
diseases = f.read()
diseases = json.loads(diseases)
f.close()

def diseaseExtractor(mainText, headline, articleDate):
    articleText = mainText
    articleHeadline = headline
    articleText = articleText.lower()
    articleHeadline = articleHeadline.lower()
    
    found = False
    add = []

    for disease in diseases:
        for element in disease['WHO']:
            element = element.lower()
            if element in articleHeadline and (found == False):
                if element == "novel" and ("2012" in articleDate or "2013" in articleDate):
                    add.append("mers-cov")
                    found = True
                elif element == "anthrax":
                    add.append("anthrax cutaneous")
                    add.append("anthrax gastrointestinous")
                    add.append("anthrax inhalation")
                    found = True
                else:
                    add.append(disease['name'])
                    found = True   

    if not found:
        for disease in diseases:
            for element in disease['WHO']:
                if element in articleText and (found == False):
                    if element == "novel" and ("2012" in articleDate or "2013" in articleDate):
                        add.append("mers-cov")
                        found = True
                    elif element == "anthrax":
                        add.append("anthrax cutaneous")
                        add.append("anthrax gastrointestinous")
                        add.append("anthrax inhalation")
                        found = True
                    else:
                        add.append(disease['name'])
                        found = True  
    
    if not found:
        add.append("unknown")

    return(add)
