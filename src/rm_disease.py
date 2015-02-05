'''
Created on 4 Feb 2015

@author: chriseisbrown
'''
import xml.sax.saxutils as saxutils
import mysql.connector
import requests
import re
from datetime import datetime

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from Disease import Disease
from EuroPMCArticle import EuroPMCArticle
from Article import Article



ABSTRACT_TABLE = "raremark.article_abstract"
ARTICLE_TABLE = "raremark.article"
DISEASE_TABLE = "raremark.disease"
MESHTERM_TABLE = "raremark.mesh_term"

ARTICLE_COLUMNS = "_id,URL,id_type,title,version,doc_version,journal,publish_date"
ABSTRACT_COLUMNS = "_id,abstract_text"
DISEASE_COLUMNS = "_id,disease_name,short_name"
MESHTERM_COLUMNS = "_id,disease_id,entry_term"

EURO_PMC_URL  = "http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=title:"
EURO_PMC_URL_EXTENSION = " src:MED pub_year:2015"

PMC_URL = "http://www.ncbi.nlm.nih.gov/pubmed/"
PMC_URL_EXTENSION = "?report=xml&format=xml"

#http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=title:"Anderson-Fabry disease","fabry" src:MED pub_year:2015

def process_hit_count(rootXML):
    hits = 0
    for elem in rootXML.iterfind('hitCount'):
        hits = int(elem.text)    
    return hits
    

def process_EuroPMC_result(rootXML):
    
    hits = process_hit_count(rootXML)
    if hits == 0:
        return
    
    euro_article_result = EuroPMCArticle()
    euro_articles_map = {}
    
    for results in rootXML.iterfind('resultList'):
        for result in results:
            euro_article_result.id = result.find('id').text
            euro_article_result.pmid = result.find('pmid').text
            euro_article_result.source = result.find('source').text
            euro_article_result.pub_year = result.find('pubYear').text
            euro_article_result.author_string = result.find('authorString').text
            euro_article_result.title = result.find('title').text
            
            euro_articles_map[euro_article_result.id] = euro_article_result
            
    return euro_articles_map


def process_PMC_result(rootXML):
    
    article = Article()
           
    for elem in rootXML.iterfind('PubmedArticle/MedlineCitation/PMID'):
        attributes = elem.attrib
        article.version = int(attributes['Version'])
        article.doc_version = attributes['Version']
        article._id = elem.text
        print article._id
        article.id_type = "PMID"
        
    for elem in rootXML.iterfind('PubmedArticle/MedlineCitation/Article/ArticleTitle'):
        article.title = elem.text
             
    for elem in rootXML.iterfind('PubmedArticle/MedlineCitation/Article/Abstract/AbstractText'):
        article.abstract_text = elem.text 
        
    for elem in rootXML.iterfind('PubmedArticle/MedlineCitation/Article/Journal/Title'):
        article.journal = elem.text 
        
    for pub_date in rootXML.iterfind('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate'):
        
        medline_date = pub_date.find('MedlineDate')
        if medline_date != None:
            print "found medline date !"
            
            medline_date_txt = medline_date.text
            
            # have we a half-decent format ?
            p1 = re.compile('^\d{4} ([A-Z][a-z]{2}-[A-Z][a-z]{2})')
            m1 = p1.match(medline_date_txt)
            
            # TODO: default this for now and sort out later
            if m1 is not None:
                month_span = m1.group(1)
                month = "Apr"
            else:
                month = "Dec"
            
            p2 = re.compile('^\d{4}')
            m2 = p2.match(medline_date_txt)
            year = m2.group()
            if year is None:
                year = "1900"
                
            day = "01"
            
        else:
            year = pub_date.find('Year')
            if year is None:
                year = "1900"
            else:
                year = year.text
            
            month = pub_date.find('Month')
            if month is None:
                month = "Jan"
            else:
                month = month.text
              
            day = pub_date.find('Day')
            if day is None:
                day = "01"
            else:
                day = day.text
              
        published_date = datetime.strptime(year + ' ' + month + ' ' + day, '%Y %b %d' ).date()
        article.publish_date = published_date.isoformat()  
        
    return article

    
            

def main():
    cnx = mysql.connector.connect(user='root', database='raremark')
    cursor = cnx.cursor()
    
    disease_query = ("select {} from {}").format(DISEASE_COLUMNS, DISEASE_TABLE)
    cursor.execute(disease_query)
    
    disease = []
    
    for(_id,disease_name,short_name) in cursor:
        d = Disease()
        d._id = _id
        d.name = disease_name
        d.short_name = short_name
        disease.append(d)
        
    for dis in disease:
        print dis.short_name        
        mesh_term_query = ("select entry_term from {} where disease_id= %(disease_id)s").format(MESHTERM_TABLE)
        cursor.execute(mesh_term_query, {'disease_id' : dis._id})
        for entry_term in cursor:
            dis.mesh_category.append(entry_term)
        
        category_list = []
        for category in dis.mesh_category:
            cat = category[0]
            dbl_quote = '"'
            quoted_category = dbl_quote + cat + dbl_quote 
            category_list.append(quoted_category)
        
        category_query = ",".join(category_list)
        
        URL = EURO_PMC_URL + category_query + EURO_PMC_URL_EXTENSION 
        print URL
        results = requests.get(URL)            
        assert results.status_code == 200  
        
        # need to unescape data that was returned
        raw_txt = results.content
        txt = saxutils.unescape(raw_txt)
        
        root = ET.fromstring(txt)
        results = process_EuroPMC_result(root)
        
        if bool(results):
            articles_map = {}
            
            for result_id in results.iterkeys():
                URL = PMC_URL + result_id + PMC_URL_EXTENSION
                print URL
                results = requests.get(URL)            
                assert results.status_code == 200  
                
                # need to unescape data that was returned
                raw_txt = results.content
                txt = saxutils.unescape(raw_txt)
                
                root = ET.fromstring(txt)
                result = process_PMC_result(root)
                
                result.URL = PMC_URL + result_id
                    
                articles_map[result._id] = result
    
            
    
    cursor.close()
    cnx.close()
    
if __name__ == "__main__":
    main()
    
    
    

      
                
