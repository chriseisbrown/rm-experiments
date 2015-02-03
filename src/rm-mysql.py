'''
Created on 1 Feb 2015

@author: chriseisbrown
'''
import mysql.connector
from Article import Article

ABSTRACT_TABLE = "raremark.article_abstract"
ARTICLE_TABLE = "raremark.article"
ARTICLE_COLUMNS = "_id,URL,id_type,title,version,doc_version,journal,publish_date"
ABSTRACT_COLUMNS = "_id,abstract_text"

cnx = mysql.connector.connect(user='root', database='raremark')
#cnx = mysql.connector.connect(user="myuser", host='localhost', database='raremark')

cursor = cnx.cursor()
#query = ('show tables')
#query=("GRANT ALL ON raremark.* TO 'myuser'@'localhost'")


article = Article()
article._id ="996"
article.URL = "http://www.ncbi.nlm.nih.gov/pubmed/25385939"
article.id_type = "TYPE"
article.title = "something with include's apostrophe"
article.version = 1
article.doc_version = "1.2"
article.abstract_text = "some abstract nonsense's have been placed here"
article.journal = "journal of something"
article.publish_date = "2014-01-03"

insert_article_query = ("INSERT INTO {}({}) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE \
    _id =VALUES(_id),URL =VALUES(URL),id_type =VALUES(id_type),title =VALUES(title),version =VALUES(version), \
    doc_version =VALUES(doc_version),journal =VALUES(journal),publish_date =VALUES(publish_date)"
    .format(ARTICLE_TABLE, ARTICLE_COLUMNS))
cursor.execute(insert_article_query, (article._id, article.URL, article.id_type, article.title,
                           article.version, article.doc_version, article.journal, article.publish_date))

insert_abstract_query = "INSERT INTO {}({}) values(%s, %s) ON DUPLICATE KEY UPDATE \
    _id=VALUES(_id),abstract_text=VALUES(abstract_text)".format(ABSTRACT_TABLE, ABSTRACT_COLUMNS)
cursor.execute(insert_abstract_query, (article._id, article.abstract_text))             
                            
cnx.commit()

query=("SELECT * FROM raremark.article")
cursor.execute(query)
for row in cursor:
    print row


cursor.close()
cnx.close()