'''
Created on 1 Feb 2015

@author: chriseisbrown
'''
import mysql.connector
from Article import Article

ABSTRACT_TABLE = "raremark.article_abstract"
ARTICLE_TABLE = "raremark.article"

cnx = mysql.connector.connect(user='root', database='raremark')
#cnx = mysql.connector.connect(user="myuser", host='localhost', database='raremark')

cursor = cnx.cursor()
#query = ('show tables')
#query=("GRANT ALL ON raremark.* TO 'myuser'@'localhost'")


article = Article()
article._id ="996"
article.URL = "http://www.ncbi.nlm.nih.gov/pubmed/25385939"
article.id_type = "PMID"
article.title = "something with include's apostrophe"
article.version = 1
article.doc_version = "1.2"
article.abstract_text = "some abstract nonsense's"
article.journal = "journal of something"
article.publish_date = "2014-01-03"

insert_article_query = "INSERT INTO {} values(%s,%s,%s,%s,%s,%s,%s,%s)".format(ARTICLE_TABLE)
cursor.execute(insert_article_query, (article._id, article.URL, article.id_type, article.title,
                           article.version, article.doc_version, article.journal, article.publish_date))

insert_abstract_query = "INSERT INTO {} values(%s, %s)".format(ABSTRACT_TABLE)
cursor.execute(insert_abstract_query, (article._id, article.abstract_text))             
                            
cnx.commit()

query=("SELECT * FROM raremark.article")
cursor.execute(query)
for row in cursor:
    print row


cursor.close()
cnx.close()