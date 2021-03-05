import googlemaps
import pycountry_convert as pc




# Returns the 
def getGeoInformation(place):

    result = {}


    # Initialise the Google Maps client
    gmaps = googlemaps.Client(key='AIzaSyDSIF81XzGn7kCIkeLwnxXqkCP-M69ebeo')

    # Do a geocode lookup of the given place
    geocode_result = gmaps.geocode(place, language='en-AU')

    sample = ['country', 'administrative_area_level_1', 'locality']
    
    try:
    # Get the place names
        for component in geocode_result[0]['address_components']:
            #if any(x in component['types'] for x in sample):
                #result.append(component['long_name'])
                #result = result + [component['long_name']]
            if 'locality' in component['types']:
                result['city'] = component['long_name']      
            if 'administrative_area_level_1' in component['types']:
                result['state'] = component['long_name']
            if 'country' in component['types']:
                result['country'] = component['long_name'] 
                if result['country'] is None or len(result['country']) is 0: 
                    return None
            if 'country' in component['types']:
                #result.append(getCont(component['long_name']))
                result['continent'] = getCont(component['long_name'])
        print(place)
        print(result)
        return result
    except IndexError as e:
         return
                
    

def getCont(count):

    continents = {
        'NA': 'North America',
        'SA': 'South America', 
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe'
    }
    hardcoded = {
        'The Gambia': 'Africa',
        'Myanmar (Burma)': 'Asia',
        'Sint Maarten': 'North America',
        'U.S. Virgin Islands': 'North America',
        'Kosovo': 'Europe',
        'Caribbean Netherlands': 'South America',
        'The Bahamas': 'North America'
    }
    if count in hardcoded.keys():
        return hardcoded[count]

    country_code = pc.country_name_to_country_alpha2(count, cn_name_format="default")
    #print(country_code)
    if country_code is 'TL':
        continent_name = 'AS'
    else:
        continent_name = pc.country_alpha2_to_continent_code(country_code)
    #print(continent_name)
    return continents[continent_name]

def getGeoData(words, country):
    result = []
    for word in words:
        if len(country) == 1:
            word = word + ' ' + country[0]
        info = getGeoInformation(word)
        #result.append(info)
        if info != None:
            result.append(info)
    if not result and len(country) > 0:
        result.append(getGeoInformation([country]))
    return [dict(t) for t in {tuple(d.items()) for d in result}]
    



# getGeoInformation(['Sydney'])