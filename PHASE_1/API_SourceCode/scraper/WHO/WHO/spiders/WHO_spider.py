import scrapy
import json
from bs4 import BeautifulSoup
import re
import datetime
import logging

logging.basicConfig(filename='Error.log', level=logging.CRITICAL, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')


from PHASE_1.API_SourceCode.keyterms.key_terms import get_key_terms
from PHASE_1.API_SourceCode.disease.diseaseExtractor import diseaseExtractor
from PHASE_1.API_SourceCode.disease.syndromeExtractor import syndromeExtractor
from PHASE_1.API_SourceCode.dateparse.event_date import get_event_date
from PHASE_1.API_SourceCode.googlemaps.getPlaces import getPlaces, get_country
from PHASE_1.API_SourceCode.database.db import db_insert, db_urls

class WHOSpider(scrapy.Spider):
    name = "WHO"
    start_urls = [
        'https://www.who.int/csr/don/archive/year/en/',
    ]

    def parse(self, response):
        years = response.css('div.col_2-1_1 ul li a::attr(href)').getall()
        
        for year in years:
            year = response.urljoin(year)
            yield scrapy.Request(year, callback = self.parse_each_year)

    def parse_each_year(self, response):
        articleLinks = response.css('ul.auto_archive li a::attr(href)').getall()
        
        urls = db_urls()
        for articleLink in articleLinks:
            articleLink = response.urljoin(articleLink)
            if articleLink in urls: 
                continue 
            yield scrapy.Request(articleLink, callback = self.parse_individual_links)

    def parse_individual_links(self, response):            
        soup = BeautifulSoup(response.body, 'html.parser')

        headline = soup.find("h1", {"class": "headline"}).getText()

        main_text = soup.find("div", {"id": "primary"})
        
        year = int(response.xpath("//meta[@name='webit_cover_date']/@content")[0].extract()[0:4])

        month = int(response.xpath("//meta[@name='webit_cover_date']/@content")[0].extract()[5:7])

        day = int(response.xpath("//meta[@name='webit_cover_date']/@content")[0].extract()[8:10])

        d1 = datetime.datetime(year, month, day) 
        d2 = datetime.datetime(2008, 3, 18) 

        if (d1 <= d2):
            remove = main_text.find("p")
            if (remove):  
                remove.decompose() 

        remove = main_text.find_all("div")
        for div in remove:
            div.decompose()

        remove = main_text.find("ul", {"class": "list_dash"})
        if (remove):  
            remove.decompose()

        remove = main_text.find("em", {"class": "dateline"})
        if (remove):  
            remove.decompose()

        for h1 in main_text.find_all('h1'):
            h1.decompose()

        for h2 in main_text.find_all('h2'):
            h2.decompose()

        for h3 in main_text.find_all('h3'):
            h3.decompose()

        for h4 in main_text.find_all('h4'):
            h4.decompose()

        for h5 in main_text.find_all('h5'):
            h5.decompose()

        for h6 in main_text.find_all('h6'):
            h6.decompose()

        main_text = main_text.getText()

        #Remove caption maybe 1 or more * followed by text
        main_text = re.sub("\*+.*\.", '', main_text)

        #Remove sources with Source: ....
        main_text = re.sub("Source: .*\S", '', main_text)

        main_text = re.sub('\n', ' ', main_text)

        main_text = re.sub('\t', ' ', main_text)

        main_text = re.sub('\r', ' ', main_text)

        main_text = re.sub(' +', ' ', main_text)

        url = response.url 
        date_of_publication = response.xpath("//meta[@name='webit_cover_date']/@content")[0].extract()
        headline = headline.strip()
        main_text = main_text.strip()
        data = {
            'url': url,
            'date_of_publication': date_of_publication,
            'headline': headline,
            'main_text': main_text
        }
        try:
            diseases = diseaseExtractor(main_text, headline, date_of_publication)
            syndromes = syndromeExtractor(main_text)
            event_date = get_event_date(main_text, date_of_publication)
            country = get_country(headline)
            locations = getPlaces(main_text, [country])
            report = {
                'diseases': diseases,
                'syndromes': syndromes, 
                'event_date': event_date, 
                'locations': locations
            }
            key_terms = get_key_terms(headline, main_text)
            data['key_terms'] = list(set(key_terms + diseases + syndromes))
            data['reports'] = [report]
            db_insert(data)
        except Exception as e:
            logging.critical("%s %s %s" % (date_of_publication, url, e))

        # filename = response.xpath("//meta[@name='webit_cover_date']/@content")[0].extract() + " " + headline
        # filename = filename.replace('/', " ")
        
        # with open(filename + ".json", 'w') as outfile:
        #     json.dump(data, outfile, ensure_ascii = False)