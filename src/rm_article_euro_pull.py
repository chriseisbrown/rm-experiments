'''
Created on 26 Feb 2015

@author: chriseisbrown
'''
import xml.sax.saxutils as saxutils
import mysql.connector
import requests
import re
import os
import math
from datetime import datetime
from xlwt import Workbook

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

EURO_PMC_URL  = "http://www.ebi.ac.uk/europepmc/webservices/rest/search/resultType=CORE&query=title:"
EURO_PMC_URL_SRC_EXTENSION = " src:MED "
EURO_PMC_URL_YEAR_EXTENSION = " pub_year:"
EURO_PMC_URL_RESULT_TYPE_PARAM = "resultType=CORE"

YEARS = ["2014", "2015"]
#YEARS = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PMC_URL = "http://www.ncbi.nlm.nih.gov/pubmed/"
PMC_URL_EXTENSION = "?report=xml&format=xml"
# example search URL:
#http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=title:"Anderson-Fabry-disease","fabry" src:MED pub_year:2015 resultType:CORE
INPUT_DIR = "../input-data/"
OUTPUT_DIR = "../output-data/"
INPUT_FILE_NAME = "Data collection.xlsx"
OUTPUT_FILE_NAME = "pipeline_report_{}.xls".format(datetime.today().strftime("%Y-%m-%d-%H%M"))

def process_hit_count(rootXML):
    hits = 0
    for elem in rootXML.iterfind('hitCount'):
        hits = int(elem.text)    
    return hits
    

def process_EuroPMC_result(euro_articles_map, disease_name, rootXML):
    
    ''' if no hits then just return what you were given '''
    hits = process_hit_count(rootXML)
    if hits == 0:
        return euro_articles_map
    
    
    for result in rootXML.iterfind('resultList/result'):
        #for result in results:
            euro_article_result = EuroPMCArticle()
            
            euro_article_result.id = result.find('id').text
            euro_article_result.pmid = result.find('pmid').text
            euro_article_result.source = result.find('source').text
            euro_article_result.pub_year = result.find('journalInfo/yearOfPublication').text
            
            euro_article_result.author = result.find('authorString')
            if euro_article_result.author is None:
                euro_article_result.author_string = ""
            else:
                euro_article_result.author_string = result.find('authorString').text
            
            
            euro_article_result.title = result.find('title').text
            
            euro_article_result.disease_name = disease_name
            
            euro_articles_map[euro_article_result.id] = euro_article_result
            
    return euro_articles_map


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
Write out euro PMC results to spreadsheet
'''             
def write_ssheet_euro_articles(articles_map):
    wb = Workbook()
    ws = wb.add_sheet('Lit output', cell_overwrite_ok=True)
    # make header row
    ws.row(0).write(0,'id')
    ws.row(0).write(1,'disease')
    ws.row(0).write(2,'title')
    ws.row(0).write(3,'pub year')
    ws.row(0).write(4,'authors')
    ws.row(0).write(5,'source')
    ws.row(0).write(6,'PubMed id')
    #ws.row(0).write(7,'time')
    #ws.row(0).write(8,'next event 1')
    #ws.row(0).write(9,'next event 2')
        
    row_num = 1
    for k in articles_map.keys():
        euro_article = articles_map.get(k)
        #print "processing article {} {}".format(euro_article.id, euro_article.disease_name)
 
        ws.row(row_num).write(0,euro_article.id)
        ws.row(row_num).write(1,euro_article.disease_name)
        ws.row(row_num).write(2,euro_article.title)
        ws.row(row_num).write(3,euro_article.pub_year)
        ws.row(row_num).write(4,euro_article.author_string)
        ws.row(row_num).write(5,euro_article.source)
        ws.row(row_num).write(6,euro_article.pmid) 
        
        row_num += 1   
          
    output_file = os.path.join(OUTPUT_DIR, OUTPUT_FILE_NAME)
    wb.save(output_file)
    print "writing output data to file {}".format(output_file)
    return



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
        
        euro_articles_map = {}
        
        for year in YEARS:
            '''
            Use the Euro PMC RESTful service for each Mesh category for each year required 
            '''
            for category_query in category_list:
                URL = EURO_PMC_URL + category_query + EURO_PMC_URL_SRC_EXTENSION +  EURO_PMC_URL_YEAR_EXTENSION + year
                print URL
                results = requests.get(URL)            
                assert results.status_code == 200  
                
                raw_txt = results.content
                
                try:
                    root = ET.fromstring(raw_txt)
                    '''
                    Data coming back from the REST service will be paginated, 25 results to a page, deal with it
                    '''
                    hits = process_hit_count(root)
                    value = hits / 25.0
                    pages = math.ceil(value)
                except ET.ParseError as XMLerror:
                    #print raw_txt[18020:18029]
                    print "XML error processing results from Euro PMC query {}".format(XMLerror.args)
                    print "Skipping processing for {} {}".format(category_query, year)
                    pages = 0

                for i in range(0, int(pages)):
                    page = i + 1
                    URL = EURO_PMC_URL + category_query + EURO_PMC_URL_SRC_EXTENSION +  EURO_PMC_URL_YEAR_EXTENSION + year + " &page=" + str(page)
                    print URL

                    results = requests.get(URL)            
                    assert results.status_code == 200  
                
                    raw_txt = results.content
                    
                    try:
                        root = ET.fromstring(raw_txt)
                        process_EuroPMC_result(euro_articles_map, dis.name, root)
                    except ET.ParseError as XMLerror:
                        print "XML Process error {}".format(XMLerror.args)
                    


        ''' Write map contents to spreadsheet '''
        print "Found {} euro article ids for consideration".format(len(euro_articles_map.keys()))    
        write_ssheet_euro_articles(euro_articles_map)        
        
    cursor.close()
    cnx.close()
    
    end = datetime.today()
    print "Done! {}".format(end.strftime("%Y-%m-%d-%H%M"))
    
    
    
if __name__ == "__main__":
    main()
    
    
    

      
                
