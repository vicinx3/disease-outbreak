import json
import os

dirname = os.path.dirname(__file__)
f = open(os.path.join(dirname,'syndrome_list.json'), 'r')
syndromes = f.read()
syndromes = json.loads(syndromes)
f.close()

def syndromeExtractor(mainText):
    articleText = mainText.lower()
    
    foundFever = False
    syndromeList = []

    for syndrome in syndromes:
        for element in syndrome['WHO']:
            element = element.lower()
            if element in articleText:
                if element == "fever":
                    if not foundFever:
                        if "haemorrhagic fever" in articleText:
                            syndromeList.append("Haemorrhagic Fever")
                            foundFever = True
                        elif "rash" in articleText:
                            syndromeList.append("Acute fever and rash")
                            foundFever = True
                        else:
                            syndromeList.append("Fever of unknown Origin")
                            foundFever = True
                else:
                    syndromeList.append(syndrome['name'])
    
    return syndromeList