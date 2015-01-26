'''
Created on 22 Jan 2015
Experiment to pull data from Pubmed and do some simple manipulation on it.

@author: chriseisbrown
'''

import json
import requests
import pymongo
import xml.sax.saxutils as saxutils

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
from Article import Article
from datetime import datetime

# http://api.crunchbase.com/v/1/company/lyst.js?api_key=85n57qg5tsyqbfsnr32hfz9v  Ian's key
# http://api.crunchbase.com/v/1/company/lyst.js?api_key=hdrqbey978rtpejejrqya4z9  Bart's key

#client = pymongo.MongoClient()
#company_db = client.companies_database
#c = company_db.companies.find({}, {"_id" : 0, "permalink" : 1}).limit(10)


def main():
    url = "http://www.ncbi.nlm.nih.gov/pubmed/25345090?report=xml&format=xml"
    results = requests.get(url)
    assert results.status_code == 200
    
    raw_txt = results.content
    
    # need to unescape data that was returned
    txt = saxutils.unescape(raw_txt)
    
    root = ET.fromstring(txt)
    
    article = Article()

    for elem in root.iterfind('PubmedArticle/MedlineCitation/PMID'):
        attributes = elem.attrib
        article.version = int(attributes['Version'])
        article.id = elem.text
        print article.id
    
    for elem in root.iterfind('PubmedArticle/MedlineCitation/Article/Abstract/AbstractText'):
        article.abstract_text = elem.text 
        
    for elem in root.iterfind('PubmedArticle/MedlineCitation/Article/Journal/Title'):
        article.journal = elem.text 
        
    for pub_date in root.iterfind('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate'):
        year = pub_date.find('Year')
        month = pub_date.find('Month')  
        day = pub_date.find('Day')
        if day == None:
            day = "01"
        else:
            day = day.text  
        published_date = datetime.strptime(year.text + ' ' + month.text + ' ' + day, '%Y %b %d' ).date()
        article.publish_date = published_date.isoformat()  
        
    
    json_doc = json.dumps(article.__dict__)
    article.display()
    



if __name__ == "__main__":
    main()    

