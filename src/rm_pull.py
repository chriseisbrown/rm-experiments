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
    
    for child_of_root in root:
        print child_of_root.tag, child_of_root.attrib


if __name__ == "__main__":
    main()    

