keywords = ["outbreak", "infection", "fever", "virus", "epidemic", "infectious", "illness", "bacteria", "emerging", "unkown virus", 
    "mysterious disease", "mystery disease", "zika", "mers", "salmonella", "legionnaire", "measles", "anthrax", "botulism", "plague", "smallpox",
    "pox", "tularemia", "junin fever", "machupo fever", "guanarito fever", "chapare fever", "lassa fever", "lujo fever", "hantavirus",
    "rift valley fever", "crimean-congo hemorrhagic fever", "dengue", "ebola", "marburg", "unknown", "other", "anthrax cutaneous", "anthrax gastrointestinous", 
    "anthrax inhalation", "brucellosis", "chikungunya", "cholera", "cryptococcosis", "cryptosporidiosis", "diphteria", "ebola haemorrhagic fever", 
    "ehec", "e.coli", "enterovirus 71 infection", "influenza a/h5n1", "influenza a/h7n9", "influenza a/h9n2", "influenza a/h1n1", "influenza a/h1n2", 
    "influenza a/h3n5", "influenza a/h3n2", "influenza a/h2n2", "hand, foot and mouth disease", "hepatitis a", "hepatitis b", "hepatitis c", "hepatitis d", 
    "hepatitis e", "histoplasmosis", "hiv", "aids", "malaria", "mers-cov", "mumps", "nipah virus", "norovirus infection", "pertussis", "pneumococcus pneumonia", 
    "poliomyelitis", "q fever", "rabies", "rotavirus infection", "rubella", "salmonellosis", "sars", "shigellosis", "staphylococcal enterotoxin b", 
    "thypoid fever", "tuberculosis", "vaccinia", "cowpox", "varicella", "west nile virus", "yellow fever", "yersiniosis", "listeriosis", "legionares", 
    "listeriosis", "monkeypox", "2019 nCoV"]

def get_key_terms(headline, main_text):
    headline = headline.lower()
    main_text = main_text.lower()

    key_terms = []
    for word in keywords:
        if main_text.find(word) != -1 or headline.find(word) != -1:
            key_terms.append(word)
    return key_terms    