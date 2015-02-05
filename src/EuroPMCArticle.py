'''
Created on 26 Jan 2015

@author: chriseisbrown
'''
class EuroPMCArticle(object):
    def __init__(self):
        self.id = ""
        self.source = ""
        self.pmid = ""
        self.disease_name = ""
        self.title = ""
        self.pub_year = ""
        self.author_string = ""

    def display(self):
        print 'Article:', self._id, ' ', self.id_type, ' ', self.title.encode('utf-8'), ' ', self.abstract_text.encode('utf-8')
        print 'Published:', self.publish_date, ' ', self.version, ' ', self.doc_version, ' ', self.journal.encode('utf-8')

