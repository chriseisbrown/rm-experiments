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
    
    in_folder_name = INPUT_FOLDER
    in_filename = INPUT_FILENAME
    
    infile = os.path.join(in_folder_name, in_filename)    
    print "using input data from file {}".format(infile)
    
    # make publications map 
    wb = open_workbook(infile) 
    article_sheet = wb.sheet_by_name('2014')
    article_ids = article_sheet.col_values(0,1)
    article_urls = article_sheet.col_values(1,1)
    
    articles_map = {}
    i=0        
    for article_id in article_ids:  
        article = Article()
        article._id = article_id
        article.URL = article_urls[i]
        
        articles_map[article._id] = article
    
    
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
        year = pub_date.find('Year')
        month = pub_date.find('Month')  
        day = pub_date.find('Day')
        if day == None:
            day = "01"
        else:
            day = day.text  
        published_date = datetime.strptime(year.text + ' ' + month.text + ' ' + day, '%Y %b %d' ).date()
        article.publish_date = published_date.isoformat()  
        
    article.display()
    
    client = pymongo.MongoClient()
    article_db = client.raremark_database
    
    article_key = {"_id": article._id}
    
    article_db.articles.update(article_key, article.__dict__, upsert=True )


if __name__ == "__main__":
    main()    

