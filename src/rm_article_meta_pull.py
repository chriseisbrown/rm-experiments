'''
Created on 4 Feb 2015

@author: chriseisbrown
'''
import xml.sax.saxutils as saxutils
import mysql.connector
import requests
import re
import math
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
ARTICLE_ID_TABLE = "raremark.article_id"
DISEASE_TABLE = "raremark.disease"
MESHTERM_TABLE = "raremark.mesh_term"

ARTICLE_COLUMNS = "_id,disease,URL,id_type,title,version,doc_version,journal,publish_date"
ARTICLE_ID_COLUMN = "_id"
ABSTRACT_COLUMNS = "_id,abstract_text"
DISEASE_COLUMNS = "_id,disease_name,short_name"
MESHTERM_COLUMNS = "_id,disease_id,entry_term"

EURO_PMC_URL  = "http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=title:"
EURO_PMC_URL_SRC_EXTENSION = " src:MED "
EURO_PMC_URL_YEAR_EXTENSION = " pub_year:"

YEARS = [ "2005", "2006", "2007", "2008", "2009" ]
#YEARS = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PMC_URL = "http://www.ncbi.nlm.nih.gov/pubmed/"
PMC_URL_EXTENSION = "?report=xml&format=xml"

#http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=title:"Anderson-Fabry disease","fabry" src:MED pub_year:2015

def process_hit_count(rootXML):
    hits = 0
    for elem in rootXML.iterfind('hitCount'):
        hits = int(elem.text)    
    return hits
    

def process_EuroPMC_result(euro_articles_map, disease_name, rootXML):
    #euro_articles_map = {}
    hits = process_hit_count(rootXML)
    if hits == 0:
        return euro_articles_map
    
    
    for result in rootXML.iterfind('resultList/result'):
        #for result in results:
            euro_article_result = EuroPMCArticle()
            
            euro_article_result.id = result.find('id').text
            euro_article_result.pmid = result.find('pmid').text
            euro_article_result.source = result.find('source').text
            euro_article_result.pub_year = result.find('pubYear').text
            
            euro_article_result.author = result.find('authorString')
            if euro_article_result.author is None:
                euro_article_result.author_string = ""
            else:
                euro_article_result.author_string = result.find('authorString').text
            
            
            euro_article_result.title = result.find('title').text
            
            euro_article_result.disease_name = disease_name
            
            euro_articles_map[euro_article_result.id] = euro_article_result
            
    return euro_articles_map


def process_PMC_result(rootXML):   
    article = Article()
           
    for elem in rootXML.iterfind('PubmedArticle/MedlineCitation/PMID'):
        attributes = elem.attrib
        article.version = int(attributes['Version'])
        article.doc_version = attributes['Version']
        article._id = elem.text
        #print article._id
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
            
            medline_date_txt = medline_date.text
            
            # have we a half-decent date format ?
            p1 = re.compile('^\d{4} ([A-Z][a-z]{2}-[A-Z][a-z]{2})')
            m1 = p1.match(medline_date_txt)
            
            if m1 is not None:
                month_span = m1.group(1)
                month = month_span[:3]
                if  month not in MONTHS:
                    month = "Jan"   # default to Jan
            else:
                month = "Jan"
            
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
                month = "Jan"   # default to Jan
            else:
                month = month.text
                if month not in MONTHS:
                    month = "Jan" # default to Jan
              
            day = pub_date.find('Day')
            if day is None:
                day = "01"
            else:
                day = day.text
              
        published_date = datetime.strptime(year + ' ' + month + ' ' + day, '%Y %b %d' ).date()
        article.publish_date = published_date.isoformat()  
        
    return article


def write_article_db(cnx, articles_map):
    # do writes to db from map
    db_count = 0
    db_error_count = 0 
    for article in articles_map.itervalues():    
           
        insert_article_query = ("INSERT INTO {}({}) values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE \
            _id =VALUES(_id),disease=(disease),URL =VALUES(URL),id_type =VALUES(id_type),title =VALUES(title),version =VALUES(version), \
            doc_version =VALUES(doc_version),journal =VALUES(journal),publish_date =VALUES(publish_date)"
            .format(ARTICLE_TABLE, ARTICLE_COLUMNS))

        insert_abstract_query = ("INSERT INTO {}({}) values(%s, %s) ON DUPLICATE KEY UPDATE \
            _id=VALUES(_id),abstract_text=VALUES(abstract_text)"
            .format(ABSTRACT_TABLE, ABSTRACT_COLUMNS))
        
        try:
            cursor = cnx.cursor()
            cursor.execute(insert_article_query, (article._id, article.disease, article.URL, article.id_type, article.title.encode('utf-8'),
                               article.version, article.doc_version, article.journal.encode('utf-8'), article.publish_date))
            cursor.execute(insert_abstract_query, (article._id, article.abstract_text.encode('utf-8')))   
            cnx.commit()
            db_count += 1
        except mysql.connector.Error as error:
            print "Error {} attempting to upsert article {}".format(error, article._id)
            db_error_count += 1    

'''
Write any article ids that we found in the euro index
'''             
def write_db_euro_articles(cnx, articles_map):
    # do writes to db from map
    db_count = 0
    db_error_count = 0 
    for articleId in articles_map.iterkeys():    
           
        insert_euro_article_query = ("insert into {}({}) values(%(_id)s) on duplicate key update _id=values(_id)"
            .format(ARTICLE_ID_TABLE, ARTICLE_ID_COLUMN))
        
        try:
            cursor = cnx.cursor()
            cursor.execute(insert_euro_article_query, {'_id':articleId})
            db_count += 1
        except mysql.connector.Error as error:
            print "Error {} attempting to upsert article_id {} into {}".format(error, articleId, ARTICLE_ID_TABLE)
            db_error_count += 1  
        
    cnx.commit() 


'''
Build a list of ids in the database to retrieve article data for
'''
def filter_euro_articles(cnx, euro_articles_map):
    db_count = 0
    db_error_count = 0 
    
    delete_euro_article_query = ("delete from {} WHERE {} in (select {} from {})"
        .format(ARTICLE_ID_TABLE, ARTICLE_ID_COLUMN, ARTICLE_ID_COLUMN, ARTICLE_TABLE))
    
    try:
        cursor = cnx.cursor()
        cursor.execute(delete_euro_article_query)
        cnx.commit()
    except mysql.connector.Error as error:
        print "Error {} attempting to delete from table {}".format(error, ARTICLE_ID_TABLE)
    

    select_euro_article_id_query = ("select {} from {}".format(ARTICLE_ID_COLUMN, ARTICLE_ID_TABLE))
    
    try:
        cursor = cnx.cursor()
        cursor.execute(select_euro_article_id_query)
        
        filtered_euro_articles_map = {}
        for _id in cursor:
            euro_article = euro_articles_map.get(str(_id[0]))
            filtered_euro_articles_map[str(_id[0])] = euro_article
            
    except mysql.connector.Error as error:
        print "Error {} attempting to select from table {}".format(error, ARTICLE_ID_TABLE)
        db_error_count += 1  

    return filtered_euro_articles_map


'''
MAIN 
''' 
def main():
    start = datetime.today()
    print start
    
    cnx = mysql.connector.connect(user='root', database='raremark')
    cursor = cnx.cursor()

    '''
    Build disease list from disease table 
    '''
    disease_query = ("select {} from {}").format(DISEASE_COLUMNS, DISEASE_TABLE)
    cursor.execute(disease_query)
    
    disease = [] 
    for(_id,disease_name,short_name) in cursor:
        d = Disease()
        d._id = _id
        d.name = disease_name
        d.short_name = short_name
        disease.append(d)
 
    '''
    For each disease get the MeSH category terms 
    '''
    for dis in disease:
        disease_start = datetime.today()
        print "*** ", dis.short_name, ":", dis.name, "{} ***".format(disease_start.strftime("%Y-%m-%d-%H%M"))        
        
        
        mesh_term_query = ("select entry_term from {} where disease_id= %(disease_id)s").format(MESHTERM_TABLE)
        cursor.execute(mesh_term_query, {'disease_id' : dis._id})
        for entry_term in cursor:
            dis.mesh_category.append(entry_term)
        
        '''
        category_list will hold all MeSH terms for this disease 
        '''
        category_list = []
        for category in dis.mesh_category:
            cat = category[0]    # because category is a tuple
            dbl_quote = '"'
            quoted_category = dbl_quote + cat + dbl_quote 
            category_list.append(quoted_category)
        #category_query = ",".join(category_list)
        
        for year in YEARS:
            '''
            Use the Euro PMC RESTful service for each Mesh category for each year required 
            '''
            for category_query in category_list:
                URL = EURO_PMC_URL + category_query + EURO_PMC_URL_SRC_EXTENSION +  EURO_PMC_URL_YEAR_EXTENSION + year
                print URL
                results = requests.get(URL)            
                assert results.status_code == 200  
                
                # need to unescape data that was returned
                raw_txt = results.content
                txt = saxutils.unescape(raw_txt)
                
                root = ET.fromstring(txt)
                
                '''
                Data coming back from the REST service will be paginated, 25 results to a page, deal with it
                '''
                hits = process_hit_count(root)
                value = hits / 25.0
                pages = math.ceil(value)

                euro_articles_map = {}
                for i in range(0, int(pages)):
                    page = i + 1
                    URL = EURO_PMC_URL + category_query + EURO_PMC_URL_SRC_EXTENSION +  EURO_PMC_URL_YEAR_EXTENSION + year + " &page=" + str(page)
                    print URL

                    results = requests.get(URL)            
                    assert results.status_code == 200  
                
                    # need to unescape data that was returned
                    raw_txt = results.content
                    txt = saxutils.unescape(raw_txt)
                    
                    try:
                        root = ET.fromstring(txt)
                        process_EuroPMC_result(euro_articles_map, dis.name, root)

                    except:
                        print "XML Process error {}"
                    
                '''
                If we get results from the EuroPMC index then go to US PubMed Central and get details
                '''
                print "Found {} euro article ids for consideration".format(len(euro_articles_map.keys()))    
                if(bool(euro_articles_map)):
                    write_db_euro_articles(cnx, euro_articles_map)
                    filtered_euro_articles_map = filter_euro_articles(cnx, euro_articles_map)                    
                    '''
                    After filtering out any we already have, add to database
                    '''
                    if bool(filtered_euro_articles_map):
                        articles_map = {}
                        for result_id in filtered_euro_articles_map.iterkeys():
                            URL = PMC_URL + result_id + PMC_URL_EXTENSION
                            results = requests.get(URL)            
                            assert results.status_code == 200  
                            
                            # need to unescape data that was returned
                            raw_txt = results.content
                            txt = saxutils.unescape(raw_txt)
                            
                            root = ET.fromstring(txt)
                            result = process_PMC_result(root)
                            
                            result.URL = PMC_URL + result_id
                            
                            '''
                            TEST
                            '''
                            thing = filtered_euro_articles_map.get(result_id)
                            if thing is None:
                                "We have a problem"
                                result.disease = "unknown"
                            else:
                                result.disease = filtered_euro_articles_map.get(result_id).disease_name
                                
                            articles_map[result._id] = result
                            
                        if bool(articles_map):
                            print "Found {} articles for the database".format(len(articles_map.keys()))    
                            write_article_db(cnx, articles_map)
                    else:
                        print "No articles found"
                
        
    cursor.close()
    cnx.close()
    
    end = datetime.today()
    elapsed = end - start
    print "Done! {}".format(end.strftime("%Y-%m-%d-%H%M"))
    
    
    
if __name__ == "__main__":
    main()
    
    
    

      
                
