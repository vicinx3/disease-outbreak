import pymongo
import json
import glob
import os
import sys
import datetime

# Functions
def setup():
    client = pymongo.MongoClient("mongodb+srv://codeonavirus:codeonavirus@codeonavirus-etwjy.mongodb.net/test?retryWrites=true&w=majority")
    # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.codeonavirus_db
    articles = db.articles
    return articles

articles = setup()

def db_import():
    # Import all .json files in the jsons folder
    # Append them to a list of dictionaries
    article_list = []
    path = os.getcwd()
    jsons = [filepath for filepath in glob.glob(path + "/jsons/*.json", recursive=True)]
    for filepath in jsons:
        with open(filepath) as f:
            data = json.load(f)
        try:
            article_list.append(data)
        except KeyError:
            print(data)
            continue
    articles.insert_many(article_list)

def db_insert(article):
    # Insert into db
    x =  articles.insert_one(article)


# Drop the article collection
def drop_articles():
    db = articles.codeonavirus_db
    db.articles.drop()

# Every date in range
def daterange(start, end):
    for n in range(int((end - start).days) + 1):
        yield start + datetime.timedelta(n)

def search_location(reports_list, location):
    if location is None:
        return True

    for report in reports_list:
        for loc in report["locations"]:
            # if "city" in loc and "city" in location and :
            #     return True
            # elif "state" in loc and "state" in location and loc["state"].lower() == location["state"].lower():
            #     return True
            # elif "country" in loc and "country" and location and loc["country"].lower() == location["country"].lower():
            #     return True
            # elif "continent" in loc and loc["continent"].lower() == location["continent"].lower():
            #     return True
            def match(tag):
                return location[tag] is "" or (tag in loc and loc[tag].lower() == location[tag].lower())
            if match("city") and match("state") and match("country") and match("continent"):
                return True
    return False

def search_key_terms(term_list, key_terms):
    if key_terms == []:
        return True 
    lowered = []
    for term in term_list:
        lowered.append(term.lower())
    for key_term in key_terms: 
        if key_term in lowered:
            return True
    return False

def search_date(date, all_dates):
    if date in all_dates:
        return True
    else:
        return False

def db_urls():
    result = articles.find({}, {"_id": 0})
    return [article["url"] for article in result]

def db_query(query_dict):
    query_res = []
    # Querying
    # find_one(query), find(query) similar to select
    # collection = setup()
    
    # y1, m1, d1 = [int(x) for x in query_dict["start_date"].split("-")]
    # y2, m2, d2 = [int(x) for x in query_dict["end_date"].split("-")]
    # start_date = datetime.datetime(y1, m1, d1)
    # end_date = datetime.datetime(y2, m2, d2)

    # if "key_terms" in query_dict:
    # if "location" in query_dict:
    key_terms = query_dict["key_terms"] if "key_terms" in query_dict else []
    location = query_dict["location"] if "location" in query_dict else None
    
    # Location, string match in headline, main_text
    all_dates = []
    for date in daterange(query_dict["start_date"], query_dict["end_date"]):
        all_dates.append(str(date.date()))
    
    # Fetch everything then sort
    result = articles.find({}, {"_id": 0})

    for article in result:
        date_match = False
        term_match = False
        location_match = False
        # if article["date_of_publication"] in all_dates:
        if search_date(article["date_of_publication"], all_dates):
            date_match = True
        
        # unable to test next two without formatted json
        if search_key_terms(article["key_terms"], key_terms):
            term_match = True

        if search_location(article["reports"], location):
            location_match = True
        
        if date_match is True and term_match is True and location_match is True:
            query_res.append(article)
        
    return query_res


def db_remove_duplicates():
    d = {}
    for url in db_urls():
        if url in d.keys():
            d[url] += 1
        else:
            d[url] = 0

    for url in d.keys():
        for i in range(0, d[url]):
            articles.delete_one({"url": url})
#---------------------------------------------------------------------------------#

# start date, end date, key terms[]
# start date, end date, location
# start date, end date, key terms[], location

# Uncomment below to insert into db when running this file
# db_insert()
# Sample query
'''
query_dict = {
    "start_date": "2020-01-01",
    "end_date": "2020-01-10",
    "location": { 
        "city": "Wuhan",
        "state/province/territory": "Hubei",
        "country": "China",
        "continent": "Asia"
    },
    "key_terms": "[virus, cough, fever]"
}
''' 
# Uncomment below to test above query
# db_query(query_dict)


# Uncomment below to drop articles
# drop_articles()
'''
Format

article = {
    date_of_publication
    url
    headline
    main_text
    reports[]
    key_terms[]
}

report = {
    diseases[]
    syndromes[]
    event_date
    locations[]
}

location = {
    city
    state/province/territory
    country
    continent
}

'''