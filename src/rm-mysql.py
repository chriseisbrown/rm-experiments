'''
Created on 1 Feb 2015

@author: chriseisbrown
'''
import mysql.connector

cnx = mysql.connector.connect(user='root', database='raremark')
#cnx = mysql.connector.connect(user="myuser", host='localhost', database='raremark')

cursor = cnx.cursor()
#query = ('show tables')
#query=("GRANT ALL ON raremark.* TO 'myuser'@'localhost'")
query=("SELECT * FROM raremark.article")



cursor.execute(query)

for row in cursor:
    print row