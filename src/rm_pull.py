'''
Created on 22 Jan 2015
Experiment to pull data from Pubmed and do some simple manipulation on it.

@author: chriseisbrown
'''
import os
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
from StringIO import  StringIO

from xlrd import open_workbook

INPUT_FOLDER = "../input-data/"
INPUT_FILENAME = "publications-summary.xlsx"


def main():
    client = pymongo.MongoClient()
    article_db = client.raremark_database
    
    in_folder_name = INPUT_FOLDER
    in_filename = INPUT_FILENAME
    
    infile = os.path.join(in_folder_name, in_filename)    
    print "using input data from file {}".format(infile)
    
    # make publications map 
    wb = open_workbook(infile) 
    article_sheet = wb.sheet_by_name('2014')
    #article_ids = article_sheet.col_values(0,1)
    article_urls = article_sheet.col_values(1,1)
    
    articles_map = {}
        
    for article_url in article_urls:  
        
        article = Article()        
        article.URL = article_url + "?report=xml&format=xml"
    
        #url = "http://www.ncbi.nlm.nih.gov/pubmed/25345090?report=xml&format=xml"
        results = requests.get( article.URL)
        assert results.status_code == 200
    
        raw_txt = results.content
        
        # need to unescape data that was returned
        txt = saxutils.unescape(raw_txt)
        
        root = ET.fromstring(txt)
    
        for elem in root.iterfind('PubmedArticle/MedlineCitation/PMID'):
            attributes = elem.attrib
            article.version = int(attributes['Version'])
            article._id = elem.text
            print article._id
            article.id_type = "PMID"
            
        for elem in root.iterfind('PubmedArticle/MedlineCitation/Article/ArticleTitle'):
            article.title = elem.text
                 
        for elem in root.iterfind('PubmedArticle/MedlineCitation/Article/Abstract/AbstractText'):
            article.abstract_text = elem.text 
            
        for elem in root.iterfind('PubmedArticle/MedlineCitation/Article/Journal/Title'):
            article.journal = elem.text 
            
        for pub_date in root.iterfind('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate'):
            
            medline_date = pub_date.find('MedlineDate')
            if medline_date != None:
                print "found medline date !"
            else:
                year = pub_date.find('Year')
                if year == None:
                    year = "1900"
                else:
                    year = year.text
                
                month = pub_date.find('Month')
                if month == None:
                    month = "Jan"
                else:
                    month = month.text
                  
                day = pub_date.find('Day')
                if day == None:
                    day = "01"
                else:
                    day = day.text
                  
            published_date = datetime.strptime(year + ' ' + month + ' ' + day, '%Y %b %d' ).date()
            article.publish_date = published_date.isoformat()  
            
        article.display()    
        articles_map[article._id] = article
        
        
    # do writes to db from map
    db_count = 0 
    for article in articles_map.itervalues():
        article_db_key = {"_id": article._id}    
        article_db.articles.update(article_db_key, article.__dict__, upsert=True )
        db_count += 1
    
    print "Refreshed database with {} items".format(db_count)


if __name__ == "__main__":
    main()    

